# manager for score info db
from typing import List, Dict
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from agsearch.utils import get_text_info_db
from agsearch.utils import add_to_score_info_db
from agsearch.utils import DATA_DIR
from agsearch.text import Text
from agsearch.terminfo import TermInfo
from agsearch.searcher import Searcher


class ScoreInfo(Searcher):
    def __init__(self, termfile: str):
        self.path = termfile
        self.infos = get_text_info_db()
        self.tfidfvec = None
        self.score_infos: Dict[str, float] = {}
        self.tf_matrix = None
        self.search_results = None

    @property
    def search_terms(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def scores(self):
        sim_scores = cosine_similarity(self.tf_matrix[0], self.tf_matrix)
        sim_scores = sim_scores.reshape((-1))
        sim_scores = sim_scores[1:]
        return sim_scores

    def save_results(self):
        ""
        score_id = []
        for text_id in self.infos.keys():
            index = self.score_infos.pop(text_id)
            score = self.search_results[index]
            score_id.append((text_id, score))
        score_id.sort(key=lambda x: x[1])
        score_id = {s[0]: s[1] for s in score_id}
        score_info = {"terms": self.search_terms, "docs": score_id}
        add_to_score_info_db(score_info)

    def search(self):
        ""
        self.tfidfvec = TfidfVectorizer(
            input="filename",
            preprocessor=Text.clean_text,
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
