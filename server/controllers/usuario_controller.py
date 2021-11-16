from server.schemas import usuario_schema, token_shema
from fastapi import APIRouter, Request, Response
from server.services.usuario_service import UsuarioService
from server.repository.notificacao_repository import NotificacaoRepository
from server.services.notificacao_service import NotificacaoService
from server.dependencies.session import get_session
from server.dependencies.get_environment_cached import get_environment_cached
from server.configuration.db import AsyncSession
from fastapi import Depends, Security
from server.controllers import endpoint_exception_handler
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from server.dependencies.get_current_user import get_current_user
from server.constants.permission import RoleBasedPermission
from server.configuration.environment import Environment
from server.schemas import error_schema
from server.schemas import notificacao_schema


router = APIRouter()
usuario_router = dict(
    router=router,
    prefix="/users",
    tags=["Usuários"],
)


@router.get(
    "/me",
    response_model=usuario_schema.CurrentUserOutput,
    summary='Retorna as informações contidas no token do usuário',
    response_description='Informações contidas no token do usuário',
    responses={
        401: {
            'model': error_schema.ErrorOutput401,
        },
        422: {
            'model': error_schema.ErrorOutput422,
        },
        500: {
            'model': error_schema.ErrorOutput500
        }
    }
)
@endpoint_exception_handler
async def get_current_user(
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
):

    """
        # Descrição

        Retorna as informações do usuário atual vinculadas ao token.

        # Erros

        Segue a lista de erros, por (**error_id**, **status_code**), que podem ocorrer nesse endpoint:

        - **(INVALID_OR_EXPIRED_TOKEN, 401)**: Token de acesso inválido ou expirado.
        - **(REQUEST_VALIDATION_ERROR, 422)**: Validação padrão da requisição. O detalhamento é um JSON,
        no formato de string, contendo os erros de validação encontrados.
        - **(INTERNAL_SERVER_ERROR, 500)**: Erro interno no sistema

    """

    return UsuarioService.current_user_output(current_user)


@router.get(
    "/user/me/get-notifications",
    response_model=List[notificacao_schema.NotificacaoOutput],
    summary='Retorna todas as notificações do usuário atual',
    response_description='Retorna todas as notificações do usuário atual',
    responses={
        401: {
            'model': error_schema.ErrorOutput401,
        },
        422: {
            'model': error_schema.ErrorOutput422,
        },
        500: {
            'model': error_schema.ErrorOutput500
        }
    }
)
@endpoint_exception_handler
async def get_notifications_by_guid_usuario(
    is_read: bool,
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
    session: AsyncSession = Depends(get_session),
    environment: Environment = Depends(get_environment_cached),
):

    """
        # Descrição

        Retorna os notificações do usuário atual.
        É possível filtrar pelas notificações "lidas" ou "não lidas".

        # Erros

        Segue a lista de erros, por (**error_id**, **status_code**), que podem ocorrer nesse endpoint:

        - **(INVALID_OR_EXPIRED_TOKEN, 401)**: Token de acesso inválido ou expirado.
        - **(REQUEST_VALIDATION_ERROR, 422)**: Validação padrão da requisição. O detalhamento é um JSON,
        no formato de string, contendo os erros de validação encontrados.
        - **(INTERNAL_SERVER_ERROR, 500)**: Erro interno no sistema
    """

    notificacao_service = NotificacaoService(
        notificacao_repo=NotificacaoRepository(
            db_session=session,
            environment=environment
        ),
        environment=environment
    )

    guid_usuario = current_user.guid
    return await notificacao_service.get_notificacoes_by_guid_usuario(guid_usuario, {'is_read': is_read})


@router.put(
    "/user/me/batch-read-notifications",
    response_model=List[notificacao_schema.NotificacaoOutput],
    summary='Marca as notificações do usuário atual como lidas',
    response_description='Notificações atualizadas retornadas',
    responses={
        401: {
            'model': error_schema.ErrorOutput401,
        },
        422: {
            'model': error_schema.ErrorOutput422,
        },
        500: {
            'model': error_schema.ErrorOutput500
        }
    }
)
@endpoint_exception_handler
async def read_notifications_by_guid_usuario(
    batch_notificacao_id_input: notificacao_schema.BatchIdNotificacaoInput,
    current_user: usuario_schema.CurrentUserToken = Security(get_current_user, scopes=[]),
    session: AsyncSession = Depends(get_session),
    environment: Environment = Depends(get_environment_cached),
):

    """
        # Descrição

        Marca as notificações do usuário atual como lidas.
        As notificacções devem ser enviadas em um array de IDs.

        Note que apenas as notificações do usuário atual são alterados, independente do input.

        # Erros

        Segue a lista de erros, por (**error_id**, **status_code**), que podem ocorrer nesse endpoint:

        - **(INVALID_OR_EXPIRED_TOKEN, 401)**: Token de acesso inválido ou expirado.
        - **(REQUEST_VALIDATION_ERROR, 422)**: Validação padrão da requisição. O detalhamento é um JSON,
        no formato de string, contendo os erros de validação encontrados.
        - **(INTERNAL_SERVER_ERROR, 500)**: Erro interno no sistema
    """

    notificacao_service = NotificacaoService(
        notificacao_repo=NotificacaoRepository(
            db_session=session,
            environment=environment
        ),
        environment=environment
    )

    guid_usuario = current_user.guid
    return await notificacao_service.batch_read_notifications(
        guid_usuario, batch_notificacao_id_input.id_notificacao_list
    )

