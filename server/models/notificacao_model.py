from sqlalchemy import Column, BigInteger, String, Boolean
from server.models import NotificationBase
from server.configuration import db
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


class Notificacao(db.Base, NotificationBase):

    def __init__(self, **kwargs):
        super(Notificacao, self).__init__(**kwargs)

    __tablename__ = "tb_notificacao"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    guid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    guid_usuario = Column(UUID(as_uuid=True), nullable=False, unique=False)

    conteudo = Column(String)  # Conteúdo da notificação sugerido pelo back-end

    tipo = Column(String)  # Tipo da notificação (INTERESSE_USUARIO_PROJETO, MATCH, etc)
    json_details = Column(JSONB)  # JSON com informações relevantes à notificação

    is_read = Column(Boolean, default=False)

