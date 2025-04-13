import datetime

from fastapi import Header, HTTPException

from app.database.session import db_repo


async def get_current_user(
        token = Header()
):
    repo = db_repo.get()
    session_user = await repo.users.get_session(
        token=token
    )


    if not session_user or session_user.expiration_date < datetime.datetime.now():
        raise HTTPException(
            status_code=403,
            detail='Session expired'
        )


    return session_user.user

