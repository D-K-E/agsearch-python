# search interface
"""
New text procedure

"""
import argparse
from agsearch.smanager import SearchManager
from agsearch.corpusmanager import CorpusManager
import sys


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ancient Greek Search Engine")
    parser.add_argument(
        "update",
        help="update term info before proceeding with search"
        + " 0 not update, 1 update, 2 just update",
        type=int,
        choices=[0, 1, 2],
    )
    parser.add_argument(
        "filepath",
        help="File path that includes search terms separated by a newline character",
    )
    parser.add_argument(
        "searcher",
        help="Choose your searcher: 1->Similarity, 2->TfIdf search",
        choices=[1, 2],
        type=int,
    )
    args = parser.parse_args()
    if args.update == 1:
        cmanager = CorpusManager()
    elif args.update == 2:
        cmanager = CorpusManager()
        sys.exit(0)
    manager = SearchManager(args.filepath, choice=args.searcher)
    manager.search()
