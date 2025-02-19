from typing import List

from asyncpg import Connection

from api.domain.customer.models.customer import CustomerState
from api.domain.transaction.dao.transaction_dao import TransactionDAO
from api.domain.transaction.models.transaction import Transaction, Type
from api.shared.config import get_connection_pool
from api.shared.exceptions import TransactionDebitConstraintException


class PostgresSQLTransactionDAO(TransactionDAO):

    def __init__(self):
        self.__pool = None

    async def __get_pool(self):
        if not self.__pool:
            self.__pool = await get_connection_pool()
        return self.__pool

    async def execute(self, transaction: Transaction) -> CustomerState:
        pool = await self.__get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                customer = await self.__update_customer_balance(connection=connection, transaction=transaction)
            await self.__create_transaction(connection=connection, transaction=transaction)
        return customer

    @staticmethod
    async def __create_transaction(connection: Connection, transaction: Transaction) -> None:
        await connection.fetchrow(
            """
            INSERT INTO transactions (customer_id, value, type, description)
            VALUES ($1, $2, $3, $4);
            """,
            transaction.customer_id, transaction.value, transaction.type.value, transaction.description,
            timeout=1)

    @staticmethod
    async def __update_customer_balance(connection: Connection, transaction: Transaction) -> CustomerState:
        if transaction.type == Type.DEBIT:
            row = await connection.fetchrow(
                """
                UPDATE customer
                SET balance = balance - $1
                WHERE id = $2
                RETURNING balance, "limit";
                """,
                transaction.value, transaction.customer_id,
                timeout=1)

            if row['balance'] < row['limit'] * -1:
                raise TransactionDebitConstraintException()
        else:
            row = await connection.fetchrow(
                """
                UPDATE customer
                SET balance = balance + $1
                WHERE id = $2
                RETURNING balance, "limit";
                """,
                transaction.value, transaction.customer_id,
                timeout=1)
        return CustomerState(id=transaction.customer_id, limit=row['limit'], balance=row['balance'])

    async def find_transactions(self, customer_id: int, limit: int) -> List[Transaction]:
        pool = await self.__get_pool()
        async with pool.acquire() as connection:
            rows = await connection.fetch(
                """
                SELECT t.id, t.value, t.type, t.description, t.created_at
                FROM transactions as t
                WHERE customer_id = $1
                ORDER BY t.created_at DESC
                LIMIT $2
                """,
                customer_id, limit)
            transactions = [Transaction(id=row['id'],
                                        customer_id=customer_id,
                                        value=row['value'],
                                        type=Type(row['type']),
                                        description=row['description'],
                                        created_at=row['created_at']) for row in rows]
            return transactions
