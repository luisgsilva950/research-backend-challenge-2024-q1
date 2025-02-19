from abc import ABC
from typing import List

from api.domain.customer.models.customer import CustomerState
from api.domain.transaction.models.transaction import Transaction


class TransactionDAO(ABC):

    async def execute(self, transaction: Transaction) -> CustomerState:
        ...

    async def find_transactions(self, customer_id: int, limit: int) -> List[Transaction]:
        ...
