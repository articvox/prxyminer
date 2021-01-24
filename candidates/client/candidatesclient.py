from abc import ABC, abstractmethod
from typing import List

from candidates.candidate import Candidate


class CandidatesClient(ABC):

    @abstractmethod
    def get_candidates(self) -> List[Candidate]:
        pass
