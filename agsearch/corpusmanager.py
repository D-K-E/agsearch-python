# corpus manager for term and text info

from typing import List, Set, Dict
import pdb

from agsearch.textinfo import TextInfo
from agsearch.terminfo import TermInfo
from agsearch.text import Text
from agsearch.utils import get_text_info_db
from agsearch.utils import get_term_info_db
from agsearch.utils import save_term_info_db


class CorpusManager:
    def __init__(self):
        ""
        # pdb.set_trace()
        self.text_info_db = get_text_info_db()
        self.term_info_db = get_term_info_db()
        self.term_info_text_ids: Set[str] = set()
        self.term_info_diff: Set[str] = set()

        # --------- Init funcs -----------------
        self.get_observed_texts_from_term_info()
        self.get_term_info_diff()
        self.update_term_info_with_terms()
        save_term_info_db(self.term_info_db)

    def get_observed_texts_from_term_info(self):
        ""
        self.term_info_text_ids = set()
        for term, doc_id_counts in self.term_info_db.items():
            for doc_id in doc_id_counts.keys():
                self.term_info_text_ids.add(doc_id)

    def get_term_info_diff(self) -> None:
        ""
        text_ids = set(self.text_info_db.keys())
        text_ids = text_ids.difference(self.term_info_text_ids)
        self.term_info_diff = text_ids

    def get_new_term_counts(self) -> Dict[str, Dict[str, int]]:
        ""
        terms: Dict[str, Dict[str, int]] = {}
        for text_id in self.term_info_diff:
            info = self.text_info_db[text_id]
            tinfo = TextInfo.from_info(info, text_id)
            text = Text.from_info(info=tinfo)
            term_doc_id_counts = text.to_doc_counts()
            for term, doc_id_count in term_doc_id_counts.items():
                doc_ids = terms.get(term, None)
                if doc_ids is None:
                    terms[term] = doc_id_count
                else:
                    terms[term].update(doc_id_count)
        return terms

    def update_term_info_with_terms(self):
        ""
        terms = self.get_new_term_counts()
        for term, doc_id_count in terms.items():
            term_dict = self.term_info_db.get(term, None)
            if term_dict is None:
                self.term_info_db[term] = doc_id_count
            else:
                self.term_info_db[term].update(doc_id_count)
