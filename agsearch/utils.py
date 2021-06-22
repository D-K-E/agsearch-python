# some constants and small utility functions
import os
import sys
import json
from typing import Union, List, Dict, Any
import pdb

SOURCE_DIR = os.curdir
PROJECT_DIR = os.path.join(SOURCE_DIR, "agsearch")
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
DATA_DIR = os.path.join(ASSETS_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
NORMALIZED_DIR = os.path.join(DATA_DIR, "normalized")

TEXTINFO_DB_PATH = os.path.join(DATA_DIR, "textinfo.json")
TERMINFO_DB_PATH = os.path.join(DATA_DIR, "terminfo.json")
SCOREINFO_DB_PATH = os.path.join(DATA_DIR, "scoreinfo.json")
TFIDFINFO_DB_PATH = os.path.join(DATA_DIR, "tfidfinfo.json")

GREEK_PUNCTUATION = [",", ";", ":", ".", "·"]

# functions


def read_json(path) -> Union[dict, list]:
    jfile = None
    with open(path, "r", encoding="utf-8") as f:
        jfile = json.load(f, parse_int=int, parse_float=float)
    return jfile


def write_json(path, f: Union[dict, list]) -> None:
    with open(path, "w", encoding="utf-8") as ff:
        json.dump(f, ff, ensure_ascii=False, indent=2)


def is_dict(el: Union[dict, list]) -> dict:
    if isinstance(el, dict):
        return el
    else:
        raise ValueError("it should be a dict")


def is_list(el: Union[dict, list]) -> list:
    if isinstance(el, list):
        return el
    else:
        raise ValueError("it should be a dict")


def get_term_info_db() -> dict:
    el = read_json(TERMINFO_DB_PATH)
    return is_dict(el)


def get_text_info_db() -> dict:
    el = read_json(TEXTINFO_DB_PATH)
    return is_dict(el)


def get_score_info_db() -> List[dict]:
    el = read_json(SCOREINFO_DB_PATH)
    return is_list(el)


def get_tfidf_info_db() -> List[dict]:
    el = read_json(TFIDFINFO_DB_PATH)
    return is_list(el)


def save_term_info_db(f: dict) -> None:
    write_json(TERMINFO_DB_PATH, f)


def save_text_info_db(f: dict) -> None:
    write_json(TEXTINFO_DB_PATH, f)


def save_score_info_db(f: dict) -> None:
    write_json(SCOREINFO_DB_PATH, f)


def save_tfidf_info_db(f: list) -> None:
    write_json(TFIDFINFO_DB_PATH, f)


def update_term_info_db(info: dict) -> None:
    term_info = get_term_info_db()
    is_dict(info)
    term_info.update(info)
    save_term_info_db(term_info)


def update_text_info_db(info: dict) -> None:
    text_info = get_text_info_db()
    is_dict(info)
    text_info.update(info)
    save_text_info_db(text_info)


def add_to_text_info_db(info: dict) -> None:
    ""
    text_info = get_text_info_db()
    is_dict(info)
    ks = list(info.keys())
    for text_id in ks:
        if text_id in text_info:
            raise ValueError(
                "the textinfo database already contains the text id: " + str(text_id)
            )
    text_info.update(info)
    save_text_info_db(text_info)


def add_to_score_info_db(info: dict) -> None:
    score_info_db = get_score_info_db()
    is_dict(info)
    score_info_db.append(info)
    save_score_info_db(score_info_db)


def add_to_tfidf_info_db(info: dict) -> None:
    tfidf_info_db = get_tfidf_info_db()
    is_dict(info)
    tfidf_info_db.append(info)
    save_tfidf_info_db(tfidf_info_db)


def get_term_info(term: str) -> Union[dict, None]:
    terms = get_term_info_db()
    retval = None
    for tm, info in terms.items():
        if term in tm:
            return info
    return retval


def get_text_info(text_id: str) -> Union[dict, None]:
    texts = get_text_info_db()
    info = texts.get(text_id, None)
    return info


def get_chars_from_hexval(start: str, end: str) -> List[str]:
    ""
    starth = bytes.fromhex(start).hex()
    endh = bytes.fromhex(end).hex()
    chars: List[str] = []
    count = 0
    for hval in range(int(starth, 16), int(endh, 16) + 1):
        hexvalstr = hex(hval)  # Ex. 0xe225
        hexvalstr = hexvalstr[2:]
        count += 1
        try:
            char = bytes.fromhex(hexvalstr).decode("utf-8")
        except UnicodeDecodeError:
            continue
        chars.append(char)
    return chars


def generate_general_punctuation() -> List[str]:
    ""
    gen_start = "E28080"  # range start u2000
    gen_end = "E281AF"  # range end u206f
    return get_chars_from_hexval(gen_start, gen_end)


def generate_supplemental_punctuation() -> List[str]:
    ""
    supp_start = "E2B880"  # range u+2e00
    supp_end = "E2B9BF"  # range u+2e7f
    return get_chars_from_hexval(supp_start, supp_end)


def generate_cjk_punctuation() -> List[str]:
    ""
    cjk_start = "E38080"  # u+3000
    cjk_end = "E38080"  # u+303f
    return get_chars_from_hexval(cjk_start, cjk_end)


def generate_cuneiform_punctuation() -> List[str]:
    ""
    cunei_start = "F09291B0"  # u+12470
    cunei_end = "F09291BF"  # u+1247f
    return get_chars_from_hexval(cunei_start, cunei_end)


def generate_ideographic_punctuation() -> List[str]:
    ""
    ideo_start = "F096BFA0"  # u+16fe0
    ideo_end = "F096BFBF"  # u+16fff
    return get_chars_from_hexval(ideo_start, ideo_end)


def generate_punctuation() -> List[str]:
    "Generate punctuation list using unicode ranges"
    general = generate_general_punctuation()
    supps = generate_supplemental_punctuation()
    cjks = generate_cjk_punctuation()
    ideos = generate_ideographic_punctuation()
    return general + supps + cjks + ideos


PUNCTUATIONS = generate_punctuation()
