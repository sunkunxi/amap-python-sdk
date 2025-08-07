class AmapException(Exception):
    pass


class NotFound(AmapException):
    pass


class Timeout(AmapException):
    pass


class BadRequest(AmapException):
    pass
