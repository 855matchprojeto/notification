from pydantic import Field, BaseModel
from typing import Optional, List
from uuid import UUID as GUID


class NotificacaoInput(BaseModel):

    guid_usuario: GUID = Field(example='a4ddad94-94ee-4cdc-bce9-b5b126c9a714')
    conteudo: Optional[str]
    tipo: Optional[str]
    json_details: Optional[dict]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NotificacaoOutput(BaseModel):

    id: int = Field(example=1)
    guid: GUID = Field(example='44ddad94-94ee-4cdc-bce9-b5b126c9a714')
    guid_usuario: GUID = Field(example='a4ddad94-94ee-4cdc-bce9-b5b126c9a714')
    conteudo: Optional[str]
    tipo: Optional[str]
    json_details: Optional[dict]
    is_read: Optional[bool]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BatchIdNotificacaoInput(BaseModel):

    id_notificacao_list: List[int]

