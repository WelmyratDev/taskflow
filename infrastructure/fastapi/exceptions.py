from shared.error import ErrorType
from fastapi import status, HTTPException



ERROR_TYPE_STATUS_CODES = {
    ErrorType.BAD_REQUEST.value: status.HTTP_400_BAD_REQUEST,
    ErrorType.CLIENT_ERROR.value: status.HTTP_422_UNPROCESSABLE_CONTENT,
    ErrorType.AUTHENTICATION_ERROR.value: status.HTTP_401_UNAUTHORIZED,
    ErrorType.AUTHORIZATION_ERROR.value: status.HTTP_403_FORBIDDEN,
    ErrorType.RESOURCE_NOT_FOUND.value: status.HTTP_404_NOT_FOUND,
    ErrorType.CONFLICT.value: status.HTTP_409_CONFLICT,
    ErrorType.EXTERNAL_API_ERROR.value: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorType.INTERNAL_SERVER_ERROR.value: status.HTTP_500_INTERNAL_SERVER_ERROR,
    ErrorType.CONNECTION_ERROR.value: status.HTTP_503_SERVICE_UNAVAILABLE,
    ErrorType.SERVER_BUSY_ERROR.value: status.HTTP_429_TOO_MANY_REQUESTS,
    ErrorType.NOT_IMPLEMENTED.value: status.HTTP_501_NOT_IMPLEMENTED,
}



class AppException(HTTPException):


    def __init__(
        self,
        loc: list[str] | None = None,
        msg: str | None = None,
        type: str = ErrorType.CLIENT_ERROR.value
    ):
        if not loc:
            loc = ["unknown_location"]
        
        if not msg:
            msg = f'An error occurred: {type}'

        super().__init__(
                detail={
                    'detail': [
                        {
                            'loc': loc,
                            'msg': msg[:500],
                            'type': type,
                        },
                    ],
                },
                status_code=ERROR_TYPE_STATUS_CODES[type],
            )
