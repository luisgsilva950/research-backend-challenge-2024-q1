from collections import namedtuple
from datetime import datetime

from api.domain.transaction.models.transaction import to_dict

BankStatement = namedtuple('BankStatement', ['customer', 'transactions'])


def to_dto(bank_statement: BankStatement) -> dict:
    return {'saldo': {'total': bank_statement.customer.balance,
                      'limite': bank_statement.customer.limit,
                      'data_extrato': datetime.utcnow().isoformat()},
            'ultimas_transacoes': [to_dict(transaction=t) for t in bank_statement.transactions]}
