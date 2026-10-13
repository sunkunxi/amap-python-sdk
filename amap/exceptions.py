class AmapException(Exception):
    pass


class AmapAPIError(AmapException):
    """An error reported in an Amap Web Service API response."""

    def __init__(self, response: dict[str, object]) -> None:
        self.response = response
        self.info = response.get("info", None)
        self.infocode = response.get("infocode", None)

        details = []
        if self.infocode is not None:
            details.append(f"infocode={self.infocode}")
        if self.info is not None:
            details.append(f"info={self.info}")

        message = "Amap API request failed"
        if details:
            message += f" ({', '.join(details)})"
        super().__init__(message)


class AmapTimeoutError(AmapException):
    """A synchronous or asynchronous Amap request exceeded its timeout."""

    pass
