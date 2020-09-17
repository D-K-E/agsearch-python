# text info object

from agsearch.utils import update_text_info_db
from agsearch.utils import get_text_info


class TextInfo:
    def __init__(
        self,
        text_id: str,
        has_chunks: bool,
        local_path: str,
        chunk_separator: str = "\n",
        url: str = "",
    ):
        self.text_id = text_id
        self.has_chunks = has_chunks
        self.local_path = local_path
        self.chunk_separator = chunk_separator
        self.url = url

    def __str__(self):
        return "text info: id {0}, path {1}".format(self.text_id, self.local_path)

    def save(self):
        "save term info to term info db"
        info = {self.text_id: {}}
        info[self.text_id]["has_chunks"] = self.has_chunks
        info[self.text_id]["local_path"] = self.local_path
        info[self.text_id]["chunk_separator"] = self.chunk_separator
        info[self.text_id]["url"] = self.url
        update_text_info_db(info=info)

    @classmethod
    def from_text_id(cls, text_id: str):
        ""
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
        tinfo = TextInfo(
            text_id=text_id,
            has_chunks=info["has_chunks"],
            local_path=info["local_path"],
            chunk_separator=info["chunk_separator"],
            url=info["url"],
        )
        return tinfo
