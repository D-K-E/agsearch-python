"""!
\file textinfo.py

Text info data base member
"""
# text info object

from agsearch.utils import update_text_info_db
from agsearch.utils import get_text_info


class TextInfo:
    """!
    Text info database member specified by several parameters.
    """

    def __init__(
        self,
        text_id: str,
        has_chunks: bool,
        local_path: str,
        chunk_separator: str = "\n",
        url: str = "",
    ):
        """!
        \brief constructor for text info
        \param text_id identifier of the given text
        \param has_chunks specifies whether a given text has more than one chunk
        \param local_path local path to the text document
        \param chunk_separator separator of chunks for document.
        \param url specifies the url of text if it comes from web.
        """
        self.text_id = text_id
        self.has_chunks = has_chunks
        self.local_path = local_path
        self.chunk_separator = chunk_separator
        self.url = url

    def __str__(self):
        """!
        \brief string representation of texts
        """
        return "text info: id {0}, path {1}".format(self.text_id, self.local_path)

    def save(self):
        """!
        \brief save text info to text info db

        We create a dictionary representation of the current text info member.
        Then save it to text id.
        """
        info = {self.text_id: {}}
        info[self.text_id]["has_chunks"] = self.has_chunks
        info[self.text_id]["local_path"] = self.local_path
        info[self.text_id]["chunk_separator"] = self.chunk_separator
        info[self.text_id]["url"] = self.url
        update_text_info_db(info=info)

    @classmethod
    def from_text_id(cls, text_id: str):
        """!
        \brief create text info object using text id for documents inside database

        \param text_id identifier of documents
        """
        info = get_text_info(text_id)
        if info is None:
            raise KeyError(
                "text with id " + text_id + "not found in text info database"
            )
        tinfo = TextInfo(
            text_id=text_id,
            has_chunks=info["has_chunks"],
            local_path=info["local_path"],
            chunk_separator=info["chunk_separator"],
            url=info["url"],
        )
        return tinfo

    @classmethod
    def from_info(cls, info: dict, text_id: str):
        """!
        \brief create text info object from info dict and text identifier

        \param info dictionary that contains dictionary representation of the
        given text object.

        \param text_id identifier of the text object
        """
        tinfo = TextInfo(
            text_id=text_id,
            has_chunks=info["has_chunks"],
            local_path=info["local_path"],
            chunk_separator=info["chunk_separator"],
            url=info["url"],
        )
        return tinfo
