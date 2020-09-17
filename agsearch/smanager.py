# search manager with query etc
# import pdb

from agsearch.scoreinfo import ScoreInfo
from agsearch.tfidfinfo import TfIdfInfo
from agsearch.text import Text


class SearchManager:
    def __init__(self, term_path: str, choice: int):
        self.term_path = term_path
        self.searcher_choice = choice

    def read_terms(self):
        ""
        with open(self.term_path, "r", encoding="utf-8") as f:
            terms = f.readlines()
            terms = [t.strip("\n") for t in terms]
            terms = [Text.to_lower(t) for t in terms]
            terms = [Text.remove_accent(t) for t in terms]
        #
        return terms

    def search(self):
        if self.searcher_choice == 1:
            searcher = ScoreInfo(self.term_path)
        elif self.searcher_choice == 2:
            terms = self.read_terms()
            searcher = TfIdfInfo(terms=terms)
        else:
            raise ValueError("Unknown searcher")

        searcher.search()
        searcher.save_results()
