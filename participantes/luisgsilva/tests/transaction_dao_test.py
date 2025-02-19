from datetime import datetime
from unittest import IsolatedAsyncioTestCase

from api.domain.transaction.dao.postgresql_transaction_dao import PostgresSQLTransactionDAO
from api.domain.transaction.models.transaction import Transaction, Type

# Define sample transaction data
TRANSACTION_DATA = {
    'customer_id': 1,
    'value': 100.0,
    'type': Type.DEBIT.value,
    'description': 'Test',
    'created_at': datetime.now()
}


class TestTransactionDAO(IsolatedAsyncioTestCase):

    def setUp(self):
        self.__dao = PostgresSQLTransactionDAO("postgresql://postgres:1234@localhost:5432/")

    async def test_save_transaction(self):
        transaction = Transaction(**TRANSACTION_DATA)
        await self.__dao.execute(transaction)
        saved_transaction = await self.__dao.find_transactions(customer_id=transaction.customer_id, limit=1)
        assert saved_transaction[0] == transaction

    async def test_get_transactions(self):
        transaction = Transaction(**TRANSACTION_DATA)
        await self.__dao.execute(transaction)
        transactions = await self.__dao.find_transactions(transaction.customer_id, limit=1)
        assert transaction in transactions
