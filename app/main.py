from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app import routers
from app.config import Config
from app.middleware.db import db_session_middleware

app = FastAPI(
    debug=Config.misc.debug
)

app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=db_session_middleware
)

routers = [
    routers.auth.router,
    routers.user.router,
    routers.game.router
]

for router in routers:
    app.include_router(
        router=router
    )
