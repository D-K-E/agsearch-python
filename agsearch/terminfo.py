# term info object

from typing import Dict, Tuple

from agsearch.utils import update_term_info_db
from agsearch.utils import get_term_info


class TermInfo:
    def __init__(self, term: str, doc_id_counts: Dict[str, int]):
        self.term = term
        self.dcounts = doc_id_counts

    def save(self):
        "save term info to term info db"
        info = {self.term: self.dcounts}
        update_term_info_db(info=info)

    @classmethod
    def load(cls, term: str):
        ""
        info = get_term_info(term)
        if info is None:
            raise KeyError("term " + term + "not found in term info database")
        tinfo = TermInfo(term=term, doc_id_counts=info)
        return tinfo

    def update_term_info(self, doc_id: str, term_count: int):
        ""
        self.dcounts[doc_id] = term_count
        self.save()
