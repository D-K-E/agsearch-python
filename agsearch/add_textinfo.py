"""!
add new text information to textinfo.json
"""

import argparse
import os
from agsearch.utils import DATA_DIR, add_to_text_info_db
from agsearch.textinfo import TextInfo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add textinfo to database")
    parser.add_argument("text_id", help="Text Identifier for the textinfo database")
    parser.add_argument(
        "local_text_path",
        help="Text path for adding to textinfo database. It should be given relative to textinfo.json file",
    )
    parser.add_argument(
        "has_chunks",
        help="If text has chunks (columns, lines etc), we segment them during processing",
        type=int,
        choices=[0, 1],
    )
    parser.add_argument(
        "--chunk_sep",
        help="Chunk separator assumed to be newline char \\n by default",
        default="\n",
    )
    parser.add_argument("--url", help="Text url for the path")
    args = parser.parse_args()
    tpath = args.local_text_path
    tpath = os.path.join(DATA_DIR, tpath)
    if not os.path.isfile(tpath):
        raise ValueError("text path does not exist " + tpath)

    info = {
        args.text_id: {
            "has_chunks": bool(args.has_chunks),
            "chunk_separator": args.chunk_sep,
            "url": args.url,
            "local_path": args.local_text_path,
        }
    }
    add_to_text_info_db(info=info)
