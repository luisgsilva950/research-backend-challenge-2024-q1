class NotFoundException(Exception):

    def __init__(self, message: str = "Not found"):
        super().__init__(message)


class CustomerNotFoundException(NotFoundException):

    def __init__(self):
        super().__init__("Customer not found!")


class ConstraintException(Exception):

    def __init__(self, message="Constraint exception"):
        super().__init__(message)


class TransactionDebitConstraintException(ConstraintException):

    def __init__(self):
        super().__init__("The constraint of customer's limit was violated!")


class InvalidPayloadException(ConstraintException):

    def __init__(self):
        super().__init__("InvalidPayload")
