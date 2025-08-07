from typing import Literal

T_Params = dict[str, str | int | float | bool]
T_Headers = dict[str, str]

# Poi2.0 show_fields params
T_ShowFields = list[Literal["children", "business", "indoor", "navi", "photos"]]
