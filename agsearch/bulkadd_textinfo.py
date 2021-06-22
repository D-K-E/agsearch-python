"""!
Same functionality as text info this time. We add text info in bulk
"""

import argparse
import os
from agsearch.utils import DATA_DIR, read_json, add_to_text_info_db
from agsearch.textinfo import TextInfo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add bulk textinfo to database")
    parser.add_argument("info_path", help="File path to json file containing textinfo")
    args = parser.parse_args()
    tpath = args.info_path
    infos = read_json(tpath)
    key_names = ["has_chunks", "chunk_separator", "url", "local_path"]
    for k, info in infos.items():
        for key in key_names:
            if key not in info:
                raise ValueError("Text info:" + info + " does not contain key: " + key)
    add_to_text_info_db(infos)
    print("Done!")
