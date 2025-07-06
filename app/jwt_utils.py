import jwt
from fastapi import HTTPException
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError, DecodeError
from .config import JWT_SECRET


def verify_token(token: str):
    try:
        # Quitar el prefijo "Bearer " si está presente
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        # Decodificar y verificar firma del token JWT
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

        # Validar presencia mínima de información
        if not payload.get("email") or not payload.get("role"):
            raise HTTPException(status_code=403, detail="Token sin información suficiente")

        return payload

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except DecodeError:
        raise HTTPException(status_code=401, detail="Token mal formado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
