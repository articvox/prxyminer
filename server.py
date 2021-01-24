from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from candidates.client.impl.parsingcandidatesclient import ParsingCandidatesClient
from candidates.parser.impl.freeproxylist import FreeProxyListParser


class Server:

    def __init__(self):
        self.__cache: List[str] = []
        self.__client = ParsingCandidatesClient(
            source = 'https://free-proxy-list.net',
            parser = FreeProxyListParser
        )
        self.__log = logging.getLogger(__name__)
        self.__build_cache()

    def __build_cache(self) -> Server:
        self.__log.info(f'Building cache...')
        self.__cache = [c.__dict__() for c in self.__client.get_candidates()]
        self.last_cached = datetime.now()

        self.__log.info(f'Cache built (entries: {len(self.__cache)})')
        return self

    def get_candidates(self) -> List[str]:
        return self.validate().__cache

    def validate(self) -> Server:
        diff = datetime.now() - self.last_cached
        if diff.seconds > 60 * 0.25:
            self.__log.info('Cache timed out')
            self.__build_cache()

        return self

    def invalidate(self) -> Server:
        return self.__build_cache()
