from enum import Enum, auto


from shared.enum import StrEnum
from shared.logger import logger


class ErrorType(StrEnum):
    BAD_REQUEST = auto()
    CLIENT_ERROR = auto()
    AUTHENTICATION_ERROR = auto()
    AUTHORIZATION_ERROR = auto()
    RESOURCE_NOT_FOUND = auto()
    CONFLICT = auto()
    EXTERNAL_API_ERROR = auto()
    INTERNAL_SERVER_ERROR = auto()
    CONNECTION_ERROR = auto()
    SERVER_BUSY_ERROR = auto()
    NOT_IMPLEMENTED = auto()



class AppError(Exception):

    def __init__(
        self,
        loc: list[str] | None = None,
        msg: str | None = None,
        type: ErrorType = ErrorType.CLIENT_ERROR,
    ):
        if loc:
            self.loc = loc

        if not msg:
            msg = f'An error occurred: {type.value}'

        self.msg = msg[:500]
        self.type = type.value

        logger.error(self.msg)
