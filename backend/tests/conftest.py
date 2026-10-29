from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.db import _engine_for_path
from app.main import app


@pytest.fixture
def local_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    data_dir = tmp_path / "ipo-data"
    monkeypatch.setenv("IPOFA_DATA_DIR", str(data_dir))
    _engine_for_path.cache_clear()
    with TestClient(app):
        yield data_dir
    _engine_for_path.cache_clear()
    monkeypatch.delenv("IPOFA_DATA_DIR", raising=False)
