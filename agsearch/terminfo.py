"""!
\file terminfo.py 

Term info database member
"""
# term info object

from typing import Dict, Tuple

from agsearch.utils import update_term_info_db
from agsearch.utils import get_term_info


class TermInfo:
    """!
    \brief term info object
    """

    def __init__(self, term: str, doc_id_counts: Dict[str, int]):
        """!
        \brief term info constructor

        \param term term we are concerned with
        \param doc_id_counts we register which documents contain term through
        a dictionary. This can be saved to hard drive for cases where the
        object does not fit into memory.
        """
        self.term = term
        self.dcounts = doc_id_counts

    def save(self):
        """!
        \brief save term info to term info db

        Updates term info database saving the current TermInfo object members
        inside
        """
        info = {self.term: self.dcounts}
        update_term_info_db(info=info)

    @classmethod
    def load(cls, term: str):
        """!
        \brief load term info using term as an identifier.

        \warning homonymic words are counted as same in this representation
        """
        info = get_term_info(term)
        if info is None:
            raise KeyError("term " + term + "not found in term info database")
        tinfo = TermInfo(term=term, doc_id_counts=info)
        return tinfo

    def update_term_info(self, doc_id: str, term_count: int):
        """!
        \brief update database with given information

        \param doc_id document identifier
        \param term_count count of this term inside document
        """
        self.dcounts[doc_id] = term_count
        self.save()
