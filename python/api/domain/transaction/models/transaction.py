from collections import namedtuple
from enum import Enum


class Type(Enum):
    DEBIT = "d"
    CREDIT = "c"


Transaction = namedtuple('Transaction', ['id', 'customer_id', 'value', 'type', 'description', 'created_at'])


def to_dict(transaction: Transaction) -> dict:
    return {'valor': transaction.value,
            'tipo': transaction.type.value,
            'descricao': transaction.description,
            'realizada_em': transaction.created_at.isoformat()}
