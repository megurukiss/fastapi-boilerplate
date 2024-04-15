from core.exceptions import CustomException


class EventNotFoundException(CustomException):
    code = 404
    error_code = "EVENT__NOT_FOUND"
    message = "event not found"


