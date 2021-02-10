"""!
\file text.py

Represents a brut text object. Text is considered at document level
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
from greek_accentuation.characters import base
from cltk.stop.greek.stops import STOPS_LIST
from cltk.corpus.greek.alphabet import filter_non_greek


class Text:
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
    def read_text(cls, path: str) -> str:
        """!
        \brief read the content of the path and return it as a string.
        """
        txt = None
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
        return txt

    @classmethod
    def to_lower(cls, txt: str) -> str:
        """!
        \brief transform all characters of the string to lower case.

        \param txt string object
        """
        return txt.lower()

    @classmethod
    def remove_stop_words(cls, txt: str) -> str:
        """!
        \brief remove stop words starting from longer
        """
        text = txt
        slist = STOPS_LIST.copy()
        slist.sort(key=lambda x: len(x), reverse=True)
        for word in slist:
            text = text.replace(word, " ")
        return text

    @classmethod
    def remove_punk(cls, txt: str) -> str:
        """!
        \brief replace punctuations with spaces
        """
        text = txt
        for punk in PUNCTUATIONS:
            text = text.replace(punk, " ")
        return text

    @classmethod
    def remove_accent(cls, txt: str) -> str:
        """!
        \brief remove accents from ancient greek characters

        \code

        >>> Text.remove_accent(ἄρχω)
        >>> αρχω

        \endcode
        """
        txts: List[str] = []
        for t in txt:
            tclean = base(t)
            txts.append(tclean)
        return "".join(txts)

    @classmethod
    def remove_non_greek(cls, txt: str) -> str:
        """!
        \brief remove non greek characters from texts

        Using cltk's filter_non_greek() function.
        The function simply uses unicode code points to determine whether a
        given character is considered as greek or not.
        \warning this will NOT filter out sigma, omega and related characters
        as used by mathematical conventions. Their code points are determined
        to be different by unicode consortium. Make sure the text does not
        contain those.
        """
        return filter_non_greek(txt)

    @classmethod
    def remove_multiple_space(cls, txt: str):
        """!
        replace multiple space with a single space
        """
        return re.sub(r"\s+", " ", txt)

    @classmethod
    def clean_chunk(cls, txt: str):
        """!
        \brief Clean text chunk

        Cleaning implies here that we are removing non greek characters and
        replacing multiple spaces with a single space.
        """
        txt = cls.remove_non_greek(txt)
        return cls.remove_multiple_space(txt)

    @classmethod
    def clean_text(cls, text: str) -> str:
        """!
        \brief Text cleaning procedure if scikit learn procedure does not satisfy

        Text cleaning procedure for given string. It is very likely that text
        cleaning procedure of existing libraries such as scikit learn and
        others are not adapted to handle ancient greek documents, so we
        implement our own procedure. This does not handle every case that can
        be attested in the entire corpora. However it does remove any non greek
        characters if they exist and make all characters lower case for easy
        comparison. We also compare forms without accents since they are more
        or less a later adopted convention.
        """
        txt = cls.to_lower(text)
        txt = cls.remove_stop_words(txt)
        txt = cls.remove_punk(txt)
        txt = cls.remove_accent(txt)
        return txt

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
