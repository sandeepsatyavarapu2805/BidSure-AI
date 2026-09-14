from pathlib import Path

import pytest

from app.storage.local import LocalFileStorage


def test_local_storage_roundtrip(tmp_path: Path):
    storage = LocalFileStorage(tmp_path)

    storage.save("bids/test.bin", b"hello")

    assert storage.exists("bids/test.bin")
    assert storage.open("bids/test.bin") == b"hello"

    storage.delete("bids/test.bin")

    assert not storage.exists("bids/test.bin")


def test_storage_prevents_path_traversal(tmp_path: Path):
    storage = LocalFileStorage(tmp_path)

    with pytest.raises(ValueError):
        storage.save("../escape.bin", b"bad")