# abstract class for unifying tfidf search and cosine similarity

from abc import ABC, abstractmethod


class Searcher(ABC):
    @abstractmethod
    def search(self):
        raise NotImplementedError

    @abstractmethod
    def save_results(self):
        raise NotImplementedError
