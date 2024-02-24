import logging
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class ErrorModel(BaseModel):
    error: str


class ResponseException(Exception):
    content: dict | str
    code: int

    def __init__(self, content: ErrorModel | dict, code: int):
        super().__init__()
        self.content = (
            content.model_dump() if isinstance(content, ErrorModel) else content
        )
        self.code = code

    @classmethod
    def custom_status(cls, error: str, code: int):
        logger.info(f"Custom error raised: {error}")
        return cls(ErrorModel(error=error), code)

    @classmethod
    def bad_request(cls, error="Bad request"):
        logger.info(f"Bad request raised: {error}")  # Mantém nos logs o erro
        return cls(ErrorModel(error=error), 400)

    @classmethod
    def internal_server_error(cls, error="Internal Server Error"):
        logger.info(f"Internal server error raised: {error}")
        return cls(ErrorModel(error=error), 500)

    @classmethod
    def unauthorized(cls, error="Unauthorized"):
        logger.info(f"Unauthorized raised: {error}")
        return cls(ErrorModel(error=error), 401)

    @classmethod
    def forbidden(cls, error="Forbidden"):
        logger.info(f"Forbidden raised: {error}")
        return cls(ErrorModel(error=error), 403)

    @classmethod
    def not_found(cls, error="Not found"):
        logger.info(f"Not found raised: {error}")
        return cls(ErrorModel(error=error), 404)


def error_responses(*status_codes: int) -> dict[int | str, dict[str, Any]]:
    """
    Retorna o dicionário que representa os modelos de responses de erro.
    Os argumentos de entrada são os status HTTP de erro possíveis para aquela rota.

    A intenção é que o retorno dessa função seja colocado no argumento `responses` do
    router decorator de cada rota, possibilitanto uma melhor documentação de mensagens de erro.
    """
    return {code: {"model": ErrorModel} for code in status_codes}
