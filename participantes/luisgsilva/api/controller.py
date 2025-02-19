from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from api import transaction_service
from api.domain.customer.models.customer import to_dto as customer_to_dto
from api.domain.transaction.models.bank_statement import to_dto as bank_statement_to_dto
from api.domain.transaction.models.transaction import Transaction, Type
from api.shared.exceptions import NotFoundException, ConstraintException

app = FastAPI()


def start_fast_api():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)


VALID_TRANSACTION_TYPES = {Type.CREDIT.value, Type.DEBIT.value}


def check_transaction_payload(payload: dict):
    if 'descricao' not in payload or \
            not payload['descricao'] or \
            len(payload['descricao']) > 10 or \
            len(payload['descricao']) == 0 or \
            not isinstance(payload['valor'], int) or \
            payload['valor'] < 1 or \
            payload['tipo'] not in VALID_TRANSACTION_TYPES:
        raise ConstraintException()


@app.post("/clientes/{customer_id}/transacoes", response_model=None)
async def execute_transaction(request: Request, payload: dict, customer_id: int):
    try:
        check_transaction_payload(payload=payload)
        transaction = Transaction(id=None,
                                  customer_id=customer_id,
                                  value=payload['valor'],
                                  type=Type(payload['tipo']),
                                  description=payload['descricao'],
                                  created_at=None)
        customer = await transaction_service.execute(transaction=transaction)
        return customer_to_dto(customer=customer)
    except ConstraintException as ex:
        return ORJSONResponse(content=dict(error=str(ex)), status_code=422)
    except NotFoundException as ex:
        return ORJSONResponse(content=dict(error=str(ex)), status_code=404)


@app.get("/clientes/{customer_id}/extrato", response_model=None)
async def execute_transaction(request: Request, customer_id: int):
    try:
        bank_statement = await transaction_service.find_bank_statement(customer_id=customer_id)
        return bank_statement_to_dto(bank_statement=bank_statement)
    except ConstraintException as ex:
        return ORJSONResponse(content={'error': str(ex)}, status_code=422)
    except NotFoundException as ex:
        return ORJSONResponse(content={'error': str(ex)}, status_code=404)


if __name__ == '__main__':
    start_fast_api()
