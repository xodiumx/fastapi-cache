from typing import Optional, Tuple

from aiomcache import Client

from fastapi_cache.types import Backend


class MemcachedBackend(Backend):
    def __init__(self, mcache: Client):
        self.mcache = mcache

    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:
        return 3600, await self.get(key)

    async def get(self, key: str) -> Optional[bytes]:
        return await self.mcache.get(key.encode())

    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:
        await self.mcache.set(key.encode(), value, exptime=expire or 0)

    async def clear(self, _: str | None = None, key: str = "") -> bool:
        if not key:
            raise Exception("key is required")
        return await self.mcache.delete(key.encode())

