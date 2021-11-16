from server.configuration import exceptions
from jose import jwt
from typing import List, Optional
from fastapi import Request
from server.configuration.environment import Environment
from server.repository.notificacao_repository import NotificacaoRepository
from server.models.notificacao_model import Notificacao


class NotificacaoService:

    @staticmethod
    def is_read_filter(is_read: bool):
        return [
            Notificacao.is_read == is_read
        ]

    @staticmethod
    def get_filter_factory():
        return {
            "is_read": NotificacaoService.is_read_filter,
        }

    @staticmethod
    def get_filters_by_params(params_dict: dict):
        filters = []
        filter_factory = NotificacaoService.get_filter_factory()
        for key in params_dict:
            param = params_dict[key]
            if param:
                filters.extend(filter_factory[key](param))
        return filters

    def __init__(
        self,
        notificacao_repo: Optional[NotificacaoRepository] = None,
        environment: Optional[Environment] = None
    ):
        self.notificacao_repo = notificacao_repo
        self.environment = environment

    async def get_notificacoes_by_guid_usuario(self, guid_usuario: str, filter_params_dict: dict):
        filters = NotificacaoService.get_filters_by_params(filter_params_dict)
        notificacoes = await self.notificacao_repo.find_notifications_by_guid_usuario(
            guid_usuario, filters
        )
        return notificacoes

    async def batch_read_notifications(self, guid_usuario: str, ids_notificacoes: List[int]):
        notificacoes_updated = await self.notificacao_repo.batch_read_notification(guid_usuario, ids_notificacoes)
        return notificacoes_updated

