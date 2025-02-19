from typing import Annotated

from pydantic import BaseModel, StringConstraints, Field

from api.domain.transaction.models.transaction import Type


class TransactionRequestDTO(BaseModel):
    value: int = Field(alias="valor", gt=0)
    type: Type = Field(alias="tipo")
    description: Annotated[str, StringConstraints(min_length=1, max_length=10)] = Field(alias="descricao")
