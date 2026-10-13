import pytest

from pyamap import AmapAPIError, AmapException, AmapTimeoutError


@pytest.mark.parametrize(
    "error",
    [AmapException, AmapTimeoutError],
)
def test_sdk_exceptions_are_exception_types(error):
    with pytest.raises(error):
        raise error("request failed")


def test_timeout_error_inherits_from_sdk_base():
    assert issubclass(AmapTimeoutError, AmapException)


def test_amap_api_error_preserves_error_details_and_response():
    response = {
        "status": "0",
        "info": "USERKEY_PLAT_NOMATCH",
        "infocode": "10001",
    }

    error = AmapAPIError(response)

    assert error.response is response
    assert error.info == "USERKEY_PLAT_NOMATCH"
    assert error.infocode == "10001"
    assert "10001" in str(error)
    assert "USERKEY_PLAT_NOMATCH" in str(error)


def test_amap_api_error_supports_responses_without_details():
    error = AmapAPIError({"status": "0"})

    assert error.info is None
    assert error.infocode is None
    assert str(error) == "Amap API request failed"
