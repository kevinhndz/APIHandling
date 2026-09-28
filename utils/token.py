from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from core.config import settings
from core.exceptions import AccesoProhibidoError

KEY = settings.SECRET_KEY


def crear_token(user: str, id_user: int, rol: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=20)

    data = {
        "user": user,
        "id_user": id_user,
        "rol": rol,
        "exp": expires
    }

    token = jwt.encode(data, KEY, algorithm=settings.ALGORITHM)

    return token


def verificar_token(token: str):
    try:
        user_data = jwt.decode(
            token,
            KEY,
            algorithms=[settings.ALGORITHM]
        )
        return user_data

    except JWTError:
        raise AccesoProhibidoError("Session expirada")