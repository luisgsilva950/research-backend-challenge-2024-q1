from api.domain.customer.dao.customer_dao import CustomerDAO
from api.domain.customer.models.customer import CustomerState
from api.domain.transaction.dao.transaction_dao import TransactionDAO
from api.domain.transaction.models.bank_statement import BankStatement
from api.domain.transaction.models.transaction import Transaction


class TransactionService:

    def __init__(self, customer_dao: CustomerDAO, transaction_dao: TransactionDAO):
        self.__customer_dao = customer_dao
        self.__transaction_dao = transaction_dao

    async def execute(self, transaction: Transaction) -> CustomerState:
        return await self.__transaction_dao.execute(transaction=transaction)

    async def find_bank_statement(self, customer_id: int) -> BankStatement:
        customer = await self.__customer_dao.find_state(customer_id=customer_id)
        transactions = await self.__transaction_dao.find_transactions(customer_id=customer_id, limit=10)
        return BankStatement(customer=customer, transactions=transactions)
