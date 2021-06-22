"""!
\file scoreinfo.py

Score info data base member
"""
# manager for score info db
from typing import List, Dict, Optional
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from agsearch.utils import get_text_info_db
from agsearch.utils import add_to_score_info_db
from agsearch.utils import DATA_DIR
from agsearch.greekprocessing import clean_greek_text
from agsearch.textinfo import TextInfo
from agsearch.terminfo import TermInfo
from agsearch.searcher import Searcher


class ScoreInfo(Searcher):
    """!
    \brief represents a member of score info database.
    """

    def __init__(self, termfile: str):
        """!
        \brief Constructor for a score info database member

        self.tf_matrix term frequency inverse document frequency matrix.
        """
        ## path path to the term file
        self.path: str = termfile

        ## infos text info database
        self.infos: TextInfo = get_text_info_db()

        ## term frequency inverse document frequency vector.
        self.tfidfvec: np.ndarray = None

        ## score info dict representation.
        self.score_infos: Dict[str, float] = {}

        ## term frequency inverse document frequency matrix
        self.tf_matrix: Optional[np.ndarray] = None
        self.search_results: np.ndarray = None

    @property
    def search_terms(self) -> str:
        """!
        \brief Obtain search terms from given path

        We assume that search terms are inside the file pointed by the path.
        """
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def scores(self) -> np.ndarray:
        """!
        \brief compute cosine similarity in tf-idf matrix

        \return np.ndarray
        """
        sim_scores = cosine_similarity(self.tf_matrix[0], self.tf_matrix)
        sim_scores = sim_scores.reshape((-1))
        sim_scores = sim_scores[1:]
        return sim_scores

    def save_results(self) -> None:
        """!
        \brief save result to score info database

        For each text id from text infos we obtain the score of the given text
        then save it to score info dict which is then added to score info
        database.

        """
        score_id = []
        for text_id in self.infos.keys():
            index = self.score_infos.pop(text_id)
            score = self.search_results[index]
            score_id.append((text_id, score))
        score_id.sort(key=lambda x: x[1])
        score_id = {s[0]: s[1] for s in score_id}
        score_info = {"terms": self.search_terms, "docs": score_id}
        add_to_score_info_db(score_info)

    def search(self) -> None:
        """!
        \brief  compute cosine scores of search terms

        First we create the vectorizer, then from text infos we obtain local
        paths to the texts. From text identifiers we create a place for all the
        texts inside score info database. Then we add search terms and 
        create tf-idf matrix. We then proceed to compute scores for each term.

        \code

        >>> my_term_file = "~/somegreektext.txt" # contains search terms
        >>> sinfo = ScoreInfo(my_term_file)
        >>> sinfo.search()

        \endcode 
        """
        self.tfidfvec = TfidfVectorizer(
            input="filename",
            preprocessor=clean_greek_text,
            use_idf=True,
            smooth_idf=True,
        )
        self.score_infos = {}
        filenames = []
        index = 0
        for text_id, info in self.infos.items():
            local_path = info["local_path"]
            self.score_infos[text_id] = index
            text_path = os.path.join(DATA_DIR, local_path)
            filenames.append(text_path)
            index += 1

        filenames.insert(0, self.path)
        self.tf_matrix = self.tfidfvec.fit_transform(filenames)
        self.search_results = self.scores()
