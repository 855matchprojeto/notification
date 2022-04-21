from server.schemas import usuario_schema
from fastapi import APIRouter
from server.repository.notificacao_repository import NotificacaoRepository
from server.services.notificacao_service import NotificacaoService
from server.dependencies.session import get_session
from server.dependencies.get_environment_cached import get_environment_cached
from server.configuration.db import AsyncSession
from fastapi import Depends, Security
from server.controllers import endpoint_exception_handler
from server.dependencies.get_current_user import get_current_user
from server.configuration.environment import Environment
from server.schemas import error_schema
from server.schemas import notificacao_schema
from server.constants.permission import RoleBasedPermission

router = APIRouter()
notificacao_router = dict(
    router=router,
    prefix="/notification",
    tags=["Notificações"],
)


@router.post(
    "",
    response_model=notificacao_schema.NotificacaoOutput,
    summary='Insere uma notificação para um usuário',
    response_description='Insere uma notificação para um usuário',
    include_in_schema=False,
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
async def insert_notificacao(
    notificacao_input: notificacao_schema.NotificacaoInput,
    _: usuario_schema.CurrentUserToken = Security(
        get_current_user, scopes=[RoleBasedPermission.ANY_OP.value]),
    session: AsyncSession = Depends(get_session),
    environment: Environment = Depends(get_environment_cached),
):

    """
        # Descrição

        Insere uma notificação para um usuário. Apenas usuários com cargos com permissão
        'ANY_OP' (Qualquer operação) possuem a autorização para acessar essa requisiçõo
    """

    notificacao_service = NotificacaoService(
        notificacao_repo=NotificacaoRepository(
            db_session=session,
            environment=environment
        ),
        environment=environment
    )

    return await notificacao_service.insert_notification(notificacao_input)

