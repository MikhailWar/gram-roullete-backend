from fastapi import APIRouter

from app.database.session import db_repo
from app.models.user import AuthenticateBody, SuccessAuthenticate

router = APIRouter(
    tags=['Авторизация']
)


@router.post('/authenticate')
async def authenticate(
        authenticate_body: AuthenticateBody,
):

    repo = db_repo.get()

    session_auth = await repo.users.generate_session(
        initdata=authenticate_body.init_data
    )

    return SuccessAuthenticate(
        success=True,
        token=session_auth.token
    )


