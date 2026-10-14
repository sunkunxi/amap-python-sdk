# pyamap

[![Test](https://github.com/sunkunxi/pyamap/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/sunkunxi/pyamap/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/sunkunxi/pyamap/branch/main/graph/badge.svg)](https://codecov.io/gh/sunkunxi/pyamap)

[English](../README.md) | 简体中文

## 项目简介

这个仓库是一个用于调用[高德地图 Web 服务 API](https://lbs.amap.com/api/webservice/summary)的 Python 客户端。提供同步客户端，以及面向 asyncio 应用的异步客户端。

详见下面“封装的 API”部分以了解本 SDK 封装的服务。

## 安装

```bash
pip install pyamap
```

## API Key

请在[高德开放平台控制台](https://console.amap.com/dev/key/app)创建 Web 服务 API Key。

## 同步用法

推荐从同步客户端开始。各方法返回解析后的高德 JSON 字典。

```python
import os

from amap import Amap

amap = Amap(os.environ["AMAP_API_KEY"])
try:
    # POI 关键字检索
    pois = amap.place.text(
        "咖啡",
        region="上海",
        city_limit=True,
        page_size=10,
        page_num=1,
    )

    # 周边检索；坐标顺序为（经度，纬度）
    nearby = amap.place.around(
        "咖啡",
        location=("121.4737", "31.2304"),
        radius=1500,
    )

    # 多边形区域检索（首尾坐标相同以闭合区域）
    in_area = amap.place.polygon(
        ("116.4074", "39.9042"),
        ("116.4200", "39.9042"),
        ("116.4200", "39.9150"),
        ("116.4074", "39.9042"),
        keywords="博物馆",
    )

    # 根据高德 POI ID 查询详情
    poi = amap.place.detail("你的 POI_ID")

    # 其他服务
    weather = amap.weather.info("110000")
    districts = amap.district.list("北京市")
    geocode = amap.georegeo.geo("北京市朝阳区阜通东大街6号")
    reverse_geocode = amap.georegeo.regeo(("116.481488", "39.990464"))
    route = amap.direction.driving(
        ("116.481028", "39.989643"),
        ("116.434446", "39.90816"),
    )
finally:
    amap.close()
```

坐标使用 `(经度, 纬度)` 顺序。不同 API 的可选参数各不相同，完整参数请查看对应方法的文档字符串和高德官方 API 文档。

## 异步用法

`amap.aio.Amap` 提供基于 aiohttp 的 asyncio 客户端，服务方法与同步客户端保持对应。

```python
import asyncio
import os

from amap.aio import Amap


async def main():
    async with Amap(os.environ["AMAP_API_KEY"]) as amap:
        result = await amap.place.text("咖啡", region="上海")
        print(result)


asyncio.run(main())
```

## 封装的 API

本 SDK 封装了以下高德地图 Web API：

| API                     | 描述                                    | 客户端模块      |
| ----------------------- | --------------------------------------- | --------------- |
| POI 检索 (Place Search) | 关键字检索、周边、多边形检索和 POI 详情 | amap.place      |
| 天气                    | 当前天气与预报查询                      | amap.weather    |
| 行政区划                | 行政区查询与列举                        | amap.district   |
| 地理编码                | 正向地理编码与逆地理编码                | amap.georegeo   |
| 路径规划                | 驾车/步行等路线规划                     | amap.direction  |
| 距离测量                | 距离计算与距离矩阵查询                  | amap.distance   |
| 坐标转换                | 不同坐标系之间的转换                    | amap.coordinate |
| 输入提示                | 输入补全 / 联想提示                     | amap.inputtips  |
| IP 定位                 | 基于 IP 的位置查询                      | amap.ip         |
| 交通态势                | 交通状况与事件查询                      | amap.traffic    |

服务可用性、权限要求和调用限制请以高德官方文档为准。

## 错误处理

当高德返回 JSON 响应且 `"status": "0"` 时，客户端会抛出 `amap.exceptions.AmapAPIError`。异常对象提供原始响应、`info` 和 `infocode`：

```python
from amap.exceptions import AmapAPIError

try:
    result = amap.place.text("咖啡")
except AmapAPIError as exc:
    print(exc.infocode, exc.info)
    print(exc.response)
```

SDK 会保留高德返回的 `infocode`，不会根据错误码数字前缀猜测具体含义。请查阅[高德官方错误码说明](https://lbs.amap.com/api/webservice/guide/tools/info)及对应 API 文档。底层 HTTP 客户端报告请求超时时，SDK 会抛出 `amap.exceptions.AmapTimeoutError`；其他网络和 HTTP 传输异常仍由 `requests` 或 `aiohttp` 抛出。

## 运行环境

- Python `>=3.10,<4.0`
- 同步客户端使用 `requests`
- 异步客户端使用 `aiohttp`

依赖版本范围维护在 [pyproject.toml](pyproject.toml) 中。

## 参与贡献

欢迎提交贡献：

1. Fork 仓库，并为改动创建独立分支。
2. 使用 `uv sync --all-groups` 安装项目和开发依赖。
3. 使用 `uv run pytest` 运行相关测试。
4. 提交 Pull Request，并简要说明改动内容。

行为变更请同时补充或更新测试，并遵循项目现有的格式和类型标注规范。

## 许可证

MIT
