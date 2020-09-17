# simple text object

from typing import List, Dict
import os
import pdb
import re

from agsearch.textinfo import TextInfo
from agsearch.terminfo import TermInfo
from agsearch.utils import DATA_DIR
from agsearch.utils import PUNCTUATIONS
from greek_accentuation.characters import base
from cltk.stop.greek.stops import STOPS_LIST
from cltk.corpus.greek.alphabet import filter_non_greek


class Text:
    def __init__(
        self, chunks: List[str], has_chunks: bool, is_clean: bool, text_id: str
    ):
        self.chunks = chunks
        self.has_chunks = has_chunks
        self.is_clean = is_clean
        self.text_id = text_id
        self.term_freq: Dict[str, int] = {}

    @classmethod
    def read_text(cls, path: str) -> str:
        txt = None
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        return txt

    @classmethod
    def to_lower(cls, txt: str) -> str:
        return txt.lower()

    @classmethod
    def remove_stop_words(cls, txt: str) -> str:
        "remove stop words starting from longer"
        text = txt
        slist = STOPS_LIST.copy()
        slist.sort(key=lambda x: len(x), reverse=True)
        for word in slist:
            text = text.replace(word, " ")
        return text

    @classmethod
    def remove_punk(cls, txt: str) -> str:
        ""
        text = txt
        for punk in PUNCTUATIONS:
            text = text.replace(punk, " ")
        return text

    @classmethod
    def remove_accent(cls, txt: str) -> str:
        "remove accents from chars"
        txts: List[str] = []
        for t in txt:
            tclean = base(t)
            txts.append(tclean)
        return "".join(txts)

    @classmethod
    def remove_non_greek(cls, txt: str) -> str:
        ""
        return filter_non_greek(txt)

    @classmethod
    def remove_multiple_space(cls, txt: str):
        ""
        return re.sub(r"\s+", " ", txt)

    @classmethod
    def clean_chunk(cls, txt: str):
        txt = cls.remove_non_greek(txt)
        return cls.remove_multiple_space(txt)

    @classmethod
    def clean_text(cls, text: str) -> str:
        txt = cls.to_lower(text)
        txt = cls.remove_stop_words(txt)
        txt = cls.remove_punk(txt)
        txt = cls.remove_accent(txt)
        return txt

    @classmethod
    def get_terms(cls, chunks: List[str], sep: str) -> Dict[str, int]:
        ""
        terms: Dict[str, int] = {}
        for chunk in chunks:
            chunk_terms = [t.strip() for t in chunk.split(sep) if t]
            for t in chunk_terms:
                if t in terms:
                    terms[t] += 1
                else:
                    terms[t] = 1
        return terms

    @classmethod
    def from_info(cls, info: TextInfo, chunk_sep: str = " "):
        "create text from text info"
        text_id = info.text_id
        text_path = os.path.join(DATA_DIR, info.local_path)
        text = cls.read_text(text_path)
        text = cls.clean_text(text)
        terms: Dict[str, int] = {}
        chunks: List[str] = []
        if info.has_chunks:
            chunks = text.split(info.chunk_separator)
            chunks = [cls.clean_chunk(c) for c in chunks if c]
            terms = cls.get_terms(chunks, chunk_sep)
        else:
            chunks = [text]
            chunks = [cls.clean_chunk(c) for c in chunks if c]
            terms = cls.get_terms(chunks, chunk_sep)
        #
        text_obj = Text(
            chunks=chunks, has_chunks=info.has_chunks, is_clean=True, text_id=text_id
        )
        text_obj.term_freq = terms
        return text_obj

    def to_doc_counts(self) -> Dict[str, Dict[str, int]]:
        ""
        term_doc_id_counts: Dict[str, Dict[str, int]] = {}
        for term, count in self.term_freq.items():
            doc_id_count = {self.text_id: count}
            term_doc_id_counts[term] = doc_id_count
        return term_doc_id_counts
