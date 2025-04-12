import json

from aiogram.utils.web_app import check_webapp_signature, parse_webapp_init_data, WebAppInitData

from app.config import Config
from app.exceptions.auth import ExceptionInitData


def verify_token(
        init_data: str
) -> WebAppInitData:

    if check_webapp_signature(
        token=Config.bot.token,
        init_data=init_data.encode('utf-8')
    ):
        raise ExceptionInitData("Failed init data")
    init_data: WebAppInitData = parse_webapp_init_data(init_data)
    return init_data
