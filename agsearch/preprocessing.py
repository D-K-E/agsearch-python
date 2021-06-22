"""!
preprocessing text
"""
import re


from agsearch.utils import DATA_DIR
from agsearch.utils import PUNCTUATIONS
from agsearch.interfaces import AbstractPreprocessor


class Preprocessing(AbstractPreprocessor):
    ""

    def __init__(self, txt: str):
        """!
        """
        self.raw_txt = txt

    @classmethod
    def read(self, path) -> str:
        ""
        txt = None
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        return txt

    def read_text(self, path):
        ""
        return Preprocessing.read(path)

    def to_lower(self, txt: str) -> str:
        """!
        \brief transform all characters of the string to lower case.

        \param txt string object
        """
        return txt.lower()

    def remove_punk(self, txt: str) -> str:
        """!
        \brief replace punctuations with spaces
        """
        text = txt
        for punk in PUNCTUATIONS:
            text = text.replace(punk, " ")
        return text

    def remove_multiple_space(self, txt: str):
        """!
        replace multiple space with a single space
        """
        return re.sub(r"\s+", " ", txt)

    def remove_stop_words(self, txt: str) -> str:
        ""
        return txt

    def clean_chunk(self, txt: str):
        """!
        \brief Clean text chunk

        Cleaning implies here that we are removing non greek characters and
        replacing multiple spaces with a single space.
        """
        return self.remove_multiple_space(txt)

    def clean_text(self, txt: str) -> str:
        ""
        ltext = self.to_lower(txt)
        ltext = self.remove_punk(ltext)
        ltext = self.remove_multiple_space(ltext)
        return ltext


def clean_preprocessing_text(txt: str):
    ""
    proc = Preprocessing()
    return proc.clean_text(txt)
