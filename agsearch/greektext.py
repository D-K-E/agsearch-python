"""!
\file greektext.py

Represents a brut greek text object. Greek Text is considered at document level
"""
# simple text object

from typing import List, Dict
import os
import pdb
import re

from agsearch.textinfo import TextInfo
from agsearch.terminfo import TermInfo
from agsearch.utils import DATA_DIR
from agsearch.utils import PUNCTUATIONS
from agsearch.greekprocessing import GreekProcessing
from greek_accentuation.characters import base
from cltk.stop.greek.stops import STOPS_LIST
from cltk.corpus.greek.alphabet import filter_non_greek


class GreekText:
    """!
    \brief Document object that contains text string
    """

    def __init__(
        self, chunks: List[str], has_chunks: bool, is_clean: bool, text_id: str
    ):
        """!
        \brief Constructor for text/document object
        """

        ## chunks of strings attributed to text.
        self.chunks = chunks

        ## whether text has a single chunk or multiple chunks
        self.has_chunks = has_chunks

        ## whether text is cleaned up before considered as a valid document
        self.is_clean = is_clean

        ## a unique identifier for the text in the collection
        self.text_id = text_id

        ## term frequency dictionary for document
        self.term_freq: Dict[str, int] = {}

    @classmethod
    def get_terms(cls, chunks: List[str], sep: str) -> Dict[str, int]:
        """!
        \brief Obtain term count from given chunks.

        \param chunks a set of text parts.
        \param sep separator for text inside chunk

        We strip each term using sep and for each resulting non empty string we
        increment its slot in terms dictionary
        """
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
        """!
        \brief create text from text info

        \param info info we are going to use for creating text
        \param chunk_sep we assume that text inside chunk is separated by space

        Create a text/document from given text info
        """
        text_id = info.text_id
        text_path = os.path.join(DATA_DIR, info.local_path)
        text: str = GreekProcessing.read_text(text_path)
        greek_processor = GreekProcessing(text)
        text = greek_processor.clean_text(text)
        terms: Dict[str, int] = {}
        chunks: List[str] = []
        if info.has_chunks:
            chunks = text.split(info.chunk_separator)
            chunks = [greek_processor.clean_chunk(c) for c in chunks if c]
            terms = cls.get_terms(chunks, chunk_sep)
        else:
            chunks = [text]
            chunks = [greek_processor.clean_chunk(c) for c in chunks if c]
            terms = cls.get_terms(chunks, chunk_sep)
        #
        text_obj = Text(
            chunks=chunks, has_chunks=info.has_chunks, is_clean=True, text_id=text_id
        )
        text_obj.term_freq = terms
        return text_obj

    def to_doc_counts(self) -> Dict[str, Dict[str, int]]:
        """!
        \brief obtain doc per term count from term frequency dict

        From term frequency dictionary which contains term frequencies per
        document, we obtain document per term count.
        """
        term_doc_id_counts: Dict[str, Dict[str, int]] = {}
        for term, count in self.term_freq.items():
            doc_id_count = {self.text_id: count}
            term_doc_id_counts[term] = doc_id_count
        return term_doc_id_counts
