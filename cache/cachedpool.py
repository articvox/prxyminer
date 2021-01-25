from __future__ import annotations

import logging
import random
from typing import Any, List, Callable

LOG = logging.getLogger(__name__)


def size(items: List[Any]) -> str:
    return f'[SIZE: {len(items)}]'


class CachedPool:

    def __init__(self):
        self.__pool: List[Any] = []
        self.__cache: List[Any] = []
        self.__cache_provider = lambda: []

    def pool(self, pool: List[Any]) -> CachedPool:
        self.__pool = pool
        return self

    def cache(self, cache: List[Any]) -> CachedPool:
        self.__cache = cache
        return self

    def cache_provider(self, provider: Callable) -> CachedPool:
        self.__cache_provider = provider
        return self

    def schedule_rebuild(self, callback: Callable) -> CachedPool:
        callback(self.build)
        return self

    def build(self) -> CachedPool:
        self.__cache = self.__cache_provider()
        LOG.info('Cache built ' + size(self.__cache))
        self.fill_pool()
        return self

    def fill_pool(self) -> None:
        self.__pool = self.__cache
        LOG.info('Pool filled ' + size(self.__pool))
        random.shuffle(self.__pool)

    def get_next(self, count: int) -> List[Any]:
        if count > self.pool_size():
            LOG.info('Requested count larger than pool size')
            self.fill_pool()

        return self.__get_and_remove(
            count if self.pool_size() >= count else self.pool_size()
        )

    def __get_and_remove(self, count: int) -> List[Any]:
        items = self.__pool[:count]
        self.__pool = self.__pool[count:]
        return items

    def pool_size(self) -> int:
        return len(self.__pool)

    def pool_empty(self) -> bool:
        return self.pool_size() == 0
