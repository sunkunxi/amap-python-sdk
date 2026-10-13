import pytest

from pyamap.exceptions import AmapException, BadRequest, NotFound, Timeout


@pytest.mark.parametrize(
    "error",
    [AmapException, NotFound, Timeout, BadRequest],
)
def test_sdk_exceptions_are_exception_types(error):
    with pytest.raises(error):
        raise error("request failed")


def test_specific_exceptions_inherit_from_sdk_base():
    assert issubclass(NotFound, AmapException)
    assert issubclass(Timeout, AmapException)
    assert issubclass(BadRequest, AmapException)
