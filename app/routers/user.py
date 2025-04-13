from fastapi import APIRouter, Depends

from app.database.schemas.user import User
from app.database.session import db_repo
from app.depends.security import get_current_user
from app.models.user import UserBalance

router = APIRouter(
    tags=['Пользователь']
)


@router.get('/balance', response_model=UserBalance)
async def get_balance(
        user: User = Depends(get_current_user)
):
    repo = db_repo.get()
    balance = await repo.users.get_balance(user.id)
    return UserBalance(
        success=True,
        balance=balance
    )
