"""!
Abstract objects to be used as interfaces
"""
from abc import ABC, abstractmethod


class AbstractPreprocessor(ABC):
    """!
    """

    @abstractmethod
    def clean_text(self, text: str):
        """!
        Clean text
        """
        raise NotImplementedError

    @abstractmethod
    def read_text(self, path: str) -> str:
        ""
        raise NotImplementedError

    @abstractmethod
    def to_lower(self, txt: str) -> str:
        ""
        raise NotImplementedError

    @abstractmethod
    def remove_stop_words(self, txt: str) -> str:
        ""
        raise NotImplementedError

    @abstractmethod
    def remove_punk(self, txt: str) -> str:
        ""
        raise NotImplementedError

    @abstractmethod
    def remove_multiple_space(self, txt: str):
        ""
        raise NotImplementedError


class AbstractGreekPreprocessor(AbstractPreprocessor):
    """!
    """

    @abstractmethod
    def remove_accent(self, txt: str) -> str:
        ""
        raise NotImplementedError

    @abstractmethod
    def remove_non_greek(self, txt: str) -> str:
        ""
        raise NotImplementedError
