from api.domain.customer.dao.customer_dao import CustomerDAO
from api.domain.customer.models.customer import CustomerState
from api.shared.config import get_connection_pool
from api.shared.exceptions import CustomerNotFoundException


class PostgresSQLCustomerDAO(CustomerDAO):

    def __init__(self):
        self.__pool = None

    async def __get_pool(self):
        if not self.__pool:
            self.__pool = await get_connection_pool()
        return self.__pool

    async def find_state(self, customer_id: int) -> CustomerState:
        pool = await self.__get_pool()
        async with pool.acquire() as connection:
            row = await connection.fetchrow(
                """
                SELECT "limit", balance
                FROM customer
                WHERE id = $1;
                """,
                customer_id)
        if not row:
            raise CustomerNotFoundException()
        return CustomerState(id=customer_id, limit=row['limit'], balance=row['balance'])
