import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app import routers
from app.config import Config
from app.middleware.db import db_session_middleware
from app.services.single import SingleObj

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',

)
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


@app.on_event('startup')
async def on_startup():
    scheduler = AsyncIOScheduler()
    scheduler.start()
    print('start')
    SingleObj.scheduler = scheduler
