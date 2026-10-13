"""坐标工具单元测试(不需要 API key)"""

from decimal import Decimal

import pytest

from pyamap.types import _validate_one, format_coordinate, format_coordinates


class TestValidateOne:
    def test_str_ok(self):
        assert _validate_one("104.07", "longitude") == "104.07"

    def test_decimal_ok(self):
        assert _validate_one(Decimal("104.07"), "longitude") == "104.07"

    def test_max_6_decimals_ok(self):
        assert _validate_one("104.123456", "longitude") == "104.123456"

    def test_7_decimals_raise(self):
        with pytest.raises(ValueError, match="小数位超过 6"):
            _validate_one("104.1234567", "longitude")

    def test_invalid_str_raise(self):
        with pytest.raises(ValueError, match="不是有效数字"):
            _validate_one("abc", "longitude")

    def test_strip_whitespace(self):
        assert _validate_one("  104.07  ", "longitude") == "104.07"

    def test_scientific_notation_normalized(self):
        # Decimal('1E+2') -> str -> '100'(无科学计数法)
        assert _validate_one(Decimal("1E+2"), "longitude") == "100"

    def test_int_like_str(self):
        assert _validate_one("100", "longitude") == "100"

    def test_zero(self):
        assert _validate_one("0", "longitude") == "0"

    @pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity"])
    def test_non_finite_values_raise(self, value):
        with pytest.raises(ValueError, match="有限数字"):
            _validate_one(value, "longitude")


class TestFormatCoordinate:
    def test_str_pair(self):
        assert format_coordinate(("104.07", "30.66")) == "104.07,30.66"

    def test_decimal_pair(self):
        assert format_coordinate((Decimal("104.07"), Decimal("30.66"))) == "104.07,30.66"

    def test_mixed_pair(self):
        assert format_coordinate((Decimal("104.07"), "30.66")) == "104.07,30.66"

    def test_too_precise_raises(self):
        with pytest.raises(ValueError, match="小数位超过 6"):
            format_coordinate(("104.12345678", "30.66"))


class TestFormatCoordinates:
    def test_default_sep(self):
        result = format_coordinates([("104.07", "30.66"), ("104.08", "30.67")])
        assert result == "104.07,30.66|104.08,30.67"

    def test_custom_sep(self):
        # 用于驾车 waypoints: ';'
        result = format_coordinates([("104.07", "30.66"), ("104.08", "30.67")], sep=";")
        assert result == "104.07,30.66;104.08,30.67"

    def test_empty(self):
        assert format_coordinates([]) == ""

    def test_validate_propagates(self):
        with pytest.raises(ValueError, match="小数位超过 6"):
            format_coordinates([("104.07", "30.1234567")])
