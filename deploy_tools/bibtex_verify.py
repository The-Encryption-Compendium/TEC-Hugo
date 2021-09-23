#!/usr/bin/env python3

'''
Verify bibtex
'''

from argparse import ArgumentParser
from logging import basicConfig
from typing import Dict, Optional, List, Any
import sys

from bibtexparser.bparser import BibTexParser, BibDatabase # type: ignore

parser = ArgumentParser()
parser.add_argument("infile", help="BibTeX file containing the site's compendium entries.")
parser.add_argument("--loglevel", default="info", help="set the log level (default: info)")

def get_entry_id(bib_entry: Dict[str, Any]) -> str:
    'get the string ID from a bibtex entry'
    if 'ID' not in bib_entry:
        raise KeyError('entry has no ID field')
    ret = bib_entry['ID']
    if not isinstance(ret, str):
        raise TypeError(f'ID is {type(ret)}')
    return ret

def check_for_duplicate_ids(bib_db: BibDatabase) -> Optional[str]:
    'return an error string if there are any duplicate IDs'
    ids:List[str] = list(map(get_entry_id, bib_db.entries))
    dups = set()
    for name in ids:
        if ids.count(name) > 1:
            dups.add(name)
    if dups:
        return f"duplicate IDs: {dups}"
    return None

if __name__ == "__main__":
    args = parser.parse_args()
    basicConfig(level=args.loglevel.upper())
    bibtex = BibTexParser(common_strings=True)
    bibdb:BibDatabase
    with open(args.infile, 'r') as dataf:
        bibdb = bibtex.parse_file(dataf)

    duperr = check_for_duplicate_ids(bibdb)
    if duperr is not None:
        print(duperr, file=sys.stderr)
        sys.exit(1)
