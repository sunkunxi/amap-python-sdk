from unittest.mock import Mock

from amap.amap import Amap as SyncAmap


def test_sync_amap_initializes_all_agents_and_closes_session(monkeypatch):
    session = Mock()
    monkeypatch.setattr("amap.amap.requests.Session", lambda: session)

    amap = SyncAmap("key")

    for name in (
        "place",
        "weather",
        "district",
        "georegeo",
        "direction",
        "distance",
        "coordinate",
        "inputtips",
        "ip",
        "traffic",
    ):
        assert getattr(amap, name).amap is amap
    assert amap.http.api_key == "key"
    amap.close()
    session.close.assert_called_once_with()
