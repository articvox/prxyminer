import logging
import random
from typing import Callable, List, Any

from scheduler import Scheduler


class CachedPool:
    __RELOAD_S = 15

    def __init__(self, scheduler: Scheduler, data_src: Callable):
        self.__log = logging.getLogger(__name__)
        self.__scheduler = scheduler

        self.__cache = List[Any]
        self.__pool = List[Any]

        self.__src = data_src
        self.__reload()

    def __reload(self) -> None:
        self.__scheduler.schedule(CachedPool.__RELOAD_S, lambda: (
            self.__build_cache(),
            self.__replenish_pool()
        ))

    def __build_cache(self) -> None:
        self.__log.info(' * Building cache')
        self.__cache = self.__src()
        self.__log.info(f' * Cache built (entries: {len(self.__cache)})')

    def __replenish_pool(self) -> None:
        self.__log.info(' * Replenishing pool')
        self.__pool = random.sample(self.__cache, len(self.__cache))

    def invalidate(self) -> None:
        self.__log.info(' * Invalidating cached pool')

        self.__reload()

    def get_pooled(self) -> Any:
        return self.get_n_pooled(1)[0]

    def get_n_pooled(self, count: int) -> List[Any]:
        self.__log.info(f' * Candidate request (count: {count})')

        if len(self.__pool) < count:
            self.__replenish_pool()

        candidates = self.__pool[:count]
        self.__pool = self.__pool[count:]

        self.__log.info(f' * Remaining candidates: {len(self.__pool)}')
        return candidates
