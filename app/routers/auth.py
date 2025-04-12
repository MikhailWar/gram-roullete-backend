from fastapi import APIRouter

from app.models.user import AuthenticateBody

router = APIRouter()


@router.post('/authenticate')
def authenticate(
        authenticate_body: AuthenticateBody
):
    pass


