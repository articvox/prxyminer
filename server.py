from __future__ import annotations

import logging
from datetime import datetime
from typing import List

from candidates.candidate import Candidate
from candidates.client.impl.parsingcandidatesclient import ParsingCandidatesClient
from candidates.parser.impl.freeproxylist import FreeProxyListParser

import threading
import random


class Server:

    def __init__(self):
        self.__cache: List[Candidate] = []
        self.__pool: List[Candidate] = []
        self.__log = logging.getLogger(__name__)

        self.__client = ParsingCandidatesClient(
            source = 'https://free-proxy-list.net',
            parser = FreeProxyListParser
        )

        threading.Timer(60 * 30, self.__build_cache).start()

        self.__build_cache()
        self.__pool = self.__cache

    def __build_cache(self) -> Server:
        self.__log.info(f'Building cache...')

        self.last_cached = datetime.now()
        self.__cache = self.__client.get_candidates()

        self.__log.info(f'Cache built (entries: {len(self.__cache)})')
        return self

    def __get_and_remove(self) -> Candidate:
        if len(self.__pool) == 0:
            self.__pool = random.shuffle(self.__cache)

        return self.__pool.pop()

    def __get_candidate(self) -> Candidate:
        return self.__get_and_remove()

    def get_candidate(self) -> dict:
        self.__log.info(f'Candidates remaining: {len(self.__pool)}')

        return self.__get_candidate().to_json()

    def get_candidates(self) -> List[dict]:
        return [c.to_json() for c in self.__pool]

    def validate(self) -> Server:

        if len(self.__pool) == 0:
            self.__pool = random.shuffle(self.__cache)

        return self

    def invalidate(self) -> Server:
        return self.__build_cache()
