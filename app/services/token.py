import secrets


def generate_token(length=64):
    """
    Генерация безопасного токена.

    :param length: Длина токена (по умолчанию 32 символа)
    :return: Случайный токен в виде строки
    """

    return secrets.token_hex(length // 2)
