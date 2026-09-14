from pathlib import Path

from app.config import settings
from app.storage.service import StorageService


class LocalFileStorage(StorageService):
    def __init__(self, root: Path | None = None):
        self.root = (root or settings.storage_root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _resolve(self, key: str) -> Path:
        path = (self.root / key).resolve()

        if self.root not in path.parents:
            raise ValueError("Invalid storage path.")

        return path

    def save(self, key: str, content: bytes) -> Path:
        path = self._resolve(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def open(self, key: str) -> bytes:
        return self._resolve(key).read_bytes()

    def delete(self, key: str) -> None:
        path = self._resolve(key)
        if path.exists():
            path.unlink()

    def exists(self, key: str) -> bool:
        return self._resolve(key).exists()