from typing import List

from candidates.candidate import Candidate
from candidates.parser.candidatesparser import CandidatesParser
from bs4 import BeautifulSoup

LF = '\n'


def build_candidate(address: str) -> Candidate:
    address = address.split(':')

    return Candidate(
        address = address[0],
        port = int(address[1])
    )


class FreeProxyListParser(CandidatesParser):

    def __init__(self, https_only = False):
        self.https_only = https_only

    def parse(self, content: str) -> List[Candidate]:
        soup = BeautifulSoup(content, 'html.parser')
        textarea_contents: str = soup.find('textarea').get_text()

        addresses = textarea_contents[
                    textarea_contents.find(LF + LF):].strip()

        return [build_candidate(address) for address in addresses.split(LF)]
