from collections import namedtuple

Customer = namedtuple('Customer', ['id', 'name', 'limit', 'balance'])

CustomerState = namedtuple('CustomerState', ['id', 'limit', 'balance'])


def to_dto(customer: CustomerState) -> dict:
    return {'limite': customer.limit, 'saldo': customer.balance}
