# search interface
"""
New text procedure

"""
import argparse
from agsearch.smanager import SearchManager
from agsearch.corpusmanager import CorpusManager


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ancient Greek Search Engine")
    parser.add_argument(
        "update",
        help="update term info before proceeding with search",
        type=bool,
        choices=[0, 1],
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
    if args.update:
        cmanager = CorpusManager()
    manager = SearchManager(args.filepath, choice=args.searcher)
    manager.search()
