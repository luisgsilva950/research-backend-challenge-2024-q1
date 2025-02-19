from api.domain.customer.dao.postgresql_customer_dao import PostgresSQLCustomerDAO
from api.domain.transaction.dao.postgresql_transaction_dao import PostgresSQLTransactionDAO
from api.domain.transaction.service.transaction_service import TransactionService

customer_dao = PostgresSQLCustomerDAO()
transaction_dao = PostgresSQLTransactionDAO()
transaction_service = TransactionService(customer_dao=customer_dao, transaction_dao=transaction_dao)
