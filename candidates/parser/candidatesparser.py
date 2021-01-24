from abc import ABC, abstractmethod
from typing import List

from candidates.candidate import Candidate


class CandidatesParser(ABC):

    @abstractmethod
    def parse(self, content: str) -> List[Candidate]:
        pass
