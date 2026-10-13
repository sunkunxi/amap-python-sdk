from collections.abc import Sequence
from decimal import Decimal, InvalidOperation
from typing import Literal

T_Params = dict[str, str | int | float | bool]
T_Headers = dict[str, str]

T_Extensions = Literal["base", "all"]
# Poi2.0 show_fields params
T_ShowFields = list[Literal["children", "business", "indoor", "navi", "photos"]]

RequestMethods = Literal["POST", "GET", "PUT", "DELETE"]
# v3 及以下接口的输出格式(json/xml)
T_OutputFormat = Literal["json", "xml"]
# v5 接口只支持 json
T_OutputFormatV5 = Literal["json"]

# 坐标:经度在前,纬度在后,小数点后最多 6 位
Coordinate = tuple[str | Decimal, str | Decimal]
# 矩形:左下、右上两个顶点
Rectangle = tuple[Coordinate, Coordinate]


_MAX_DECIMALS = 6
"""高德 API 允许的经纬度小数位上限"""


def _validate_one(value: str | Decimal, name: str) -> str:
    """校验单值经/纬度,返回规范字符串(无科学计数法)"""
    if isinstance(value, Decimal):
        d = value
    else:
        s = str(value).strip()
        try:
            d = Decimal(s)
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(f"{name} 不是有效数字: {value!r}") from exc

    # Decimal('104.1234567').as_tuple() -> exponent=-7
    # Decimal('104.000000').as_tuple()  -> exponent=0(尾零被规范化掉了)
    # Decimal('104.070000').as_tuple() -> exponent=-6(刚好 6 位)
    exponent: int = d.as_tuple().exponent  # type: ignore[assignment]
    if exponent < -_MAX_DECIMALS:
        raise ValueError(f"{name} 小数位超过 {_MAX_DECIMALS} 位: {value} (高德 API 限制)")

    # 使用 :f 避免科学计数法(Decimal('1E+2') -> '100')
    return f"{d:f}"


def format_coordinate(coord: Coordinate, seq=",") -> str:
    """把 (lon, lat) 元组格式化为 'lon,lat' 字符串

    校验:
    - 经/纬度小数位 ≤ 6
    - 字符串可被解析为 Decimal
    """
    lon, lat = coord
    return f"{_validate_one(lon, 'longitude')}{seq}{_validate_one(lat, 'latitude')}"


def format_coordinates(
    coords: Sequence[Coordinate],
    sep: str = "|",
) -> str:
    """把一组坐标格式化为 'lon,lat<sep>lon,lat<sep>...' 字符串

    Args:
        coords: 坐标列表
        sep: 坐标对之间的分隔符,默认 '|'
            - POI 周边/距离测量/坐标转换: '|'
            - 驾车途经点 waypoints: ';'
            - 交通态势 rectangle: ';'
    """
    return sep.join(format_coordinate(c) for c in coords)
