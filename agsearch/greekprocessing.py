"""!
\file greekprocessing.py

Greek preprocessing functions
"""


from cltk.corpus.greek.alphabet import filter_non_greek
from cltk.stop.greek.stops import STOPS_LIST
from greek_accentuation.characters import base

from agsearch.utils import DATA_DIR
from agsearch.utils import PUNCTUATIONS
from agsearch.preprocessing import Preprocessing
from agsearch.interfaces import AbstractGreekPreprocessor


class GreekProcessing(Preprocessing, AbstractGreekPreprocessor):
    """!
    """

    def __init__(self, raw_txt: str):
        ""
        self.raw_txt = raw_txt

    def remove_non_greek(self, txt: str) -> str:
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

    def remove_accent(self, txt: str) -> str:
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

    def remove_stop_words(self, txt: str) -> str:
        """!
        \brief remove stop words starting from longer
        """
        text = txt
        slist = STOPS_LIST.copy()
        slist.sort(key=lambda x: len(x), reverse=True)
        for word in slist:
            text = text.replace(word, " ")
        return text

    def clean_chunk(self, txt: str):
        """!
        \brief Clean text chunk

        Cleaning implies here that we are removing non greek characters and
        replacing multiple spaces with a single space.
        """
        txt = self.remove_non_greek(txt)
        return self.remove_multiple_space(txt)

    def clean_text(self, text: str) -> str:
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
        txt = self.to_lower(text)
        txt = self.remove_stop_words(txt)
        txt = self.remove_punk(txt)
        txt = self.remove_accent(txt)
        return txt


def clean_greek_text(txt: str):
    ""
    proc = GreekProcessing(txt)
    return proc.clean_text(txt)
