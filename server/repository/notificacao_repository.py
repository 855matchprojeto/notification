from server.models.notificacao_model import Notificacao
from sqlalchemy import select, update, literal_column
from server.configuration.db import AsyncSession
from typing import Optional
from server.configuration.environment import Environment
from typing import List


class NotificacaoRepository:

    def __init__(self, db_session: AsyncSession, environment: Optional[Environment] = None):
        self.db_session = db_session
        self.environment = environment

    async def find_notifications_by_guid_usuario(self, guid_usuario: str, filters: Optional = None) -> Notificacao:
        stmt = (
            select(Notificacao).
            where(Notificacao.guid_usuario == guid_usuario)
        )
        if filters:
            stmt = stmt.where(*filters)

        query = await self.db_session.execute(stmt)
        notificacao = query.scalars().unique().first()
        return notificacao

    async def batch_read_notification(self, guid_usuario: str, id_notication_list: List[int]) -> List[Notificacao]:
        filters = [
            Notificacao.id.in_(id_notication_list),
            Notificacao.guid_usuario == guid_usuario
        ]
        stmt = (
            update(Notificacao).
            returning(literal_column('*')).
            where(*filters).
            values(
                is_read=True
            )
        )

        query = await self.db_session.execute(stmt)
        notificacoes = [Notificacao(**dict(row)) for row in query.fetchall()]
        return notificacoes

