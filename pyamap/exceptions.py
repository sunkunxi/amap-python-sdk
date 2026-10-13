class AmapException(Exception):
    pass


class AmapAPIError(AmapException):
    """An error reported in an Amap Web Service API response."""

    def __init__(self, response: dict[str, object]) -> None:
        self.response = response
        self.info = _optional_string(response.get("info"))
        self.infocode = _optional_string(response.get("infocode"))

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


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    return str(value)
