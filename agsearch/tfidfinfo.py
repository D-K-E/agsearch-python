# tf idf info db element

from typing import List, Union, Dict
import math
import pdb

from agsearch.terminfo import TermInfo
from agsearch.searcher import Searcher
from agsearch.utils import get_text_info_db
from agsearch.utils import add_to_tfidf_info_db


class TfIdfInfo(Searcher):
    def __init__(self, terms: List[str]):
        self.terms = terms
        self.infos = get_text_info_db()
        self.search_results = None

    def tf_idf_for_term(self, term: str) -> Union[Dict[str, float], None]:
        try:
            tinfo = TermInfo.load(term)
        except KeyError:
            return None
        #
        term_doc_counts = len(list(tinfo.dcounts.keys()))
        total_doc_count = len(self.infos)
        invdocFreq = math.log(total_doc_count / term_doc_counts)
        term_tf_idf_doc: Dict[str, float] = {}
        for text_id, term_freq in tinfo.dcounts.items():
            term_tf_idf_doc[text_id] = invdocFreq * term_freq
        return term_tf_idf_doc

    def get_average_score_per_term(self, tfinfos: dict) -> dict:
        ""
        nb_docs = len(self.infos)
        average_score: Dict[str, float] = {}
        for term, doc_scores in tfinfos.items():
            average_score[term] = sum(doc_scores.values()) / nb_docs
        return average_score

    def get_average_score_per_doc(self, tfinfos: dict) -> dict:
        ""
        doc_scores: Dict[str, float] = {}
        nb_terms = len(tfinfos)
        for term, doc_score in tfinfos.items():
            for doc_id, score in doc_score.items():
                if doc_id in doc_scores:
                    doc_scores[doc_id] += score / nb_terms
                else:
                    doc_scores[doc_id] = 0.0
        return doc_scores

    def average_infos(self, tidf_infos: dict) -> Dict[str, Dict[str, float]]:
        per_term = self.get_average_score_per_term(tidf_infos)
        per_doc = self.get_average_score_per_doc(tidf_infos)
        tidf_infos["average_score_per_term"] = per_term
        tidf_infos["average_score_per_document"] = per_doc
        return tidf_infos

    def search(self):
        ""
        # pdb.set_trace()
        tf_idf_infos: Dict[str, Dict[str, float]] = {}
        for term in self.terms:
            tf_idf_vals = self.tf_idf_for_term(term)
            if tf_idf_vals is None:
                continue
            tf_idf_infos[term] = tf_idf_vals
        #
        tf_idf_infos = self.average_infos(tf_idf_infos)
        self.search_results = tf_idf_infos

    def save_results(self):
        # pdb.set_trace()
        add_to_tfidf_info_db(self.search_results)
