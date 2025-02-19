from abc import ABC

from api.domain.customer.models.customer import Customer


class CustomerDAO(ABC):

    async def find_state(self, customer_id: int) -> Customer:
        ...
