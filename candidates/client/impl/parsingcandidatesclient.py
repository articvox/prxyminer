from typing import List, Type

from candidates.candidate import Candidate
from candidates.client.candidatesclient import CandidatesClient
from candidates.parser.candidatesparser import CandidatesParser


class ParsingCandidatesClient(CandidatesClient):
    import requests

    def __init__(self, source: str, parser: Type[CandidatesParser]):
        self.source = source
        self.parser = parser()

    def get_candidates(self) -> List[Candidate]:
        response = self.requests.get(self.source)
        return self.parser.parse(response.text)
