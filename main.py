#!/usr/bin/env python3

import argparse
import sys
import re
from entry import Entry
from typing import List

misc_entries = re.compile(r'@misc\{[^,]+,')
title_val    = re.compile(r'title = \{.*\},')

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return ''.join(f.readlines())


def get_misc_entries(contents: str):
    for match in misc_entries.finditer(contents):
        # start and end of match
        start, end = match.start(), match.end()

        num_parens = 1
        index = end + 1
        while num_parens > 0:
            char = contents[index]
            if char == '{':
                num_parens += 1
            elif char == '}':
                num_parens -= 1
            index += 1

        yield Entry(start, index, contents[start:index])


def transform_bib_file(source: str, entries: List[Entry], save_as: str):
    for entry in entries:
        print(entry)


def main(bibfile, placement):
    # read bibliography file into memory
    contents = read_file(bibfile)

    # get list of misc entries in bibliography file
    entries = list(get_misc_entries(contents))
    
    transform_bib_file(contents, entries, '{}-new.bib'.format(bibfile[:-4]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transforms a bibtex file '
                                                 'to render Misc entries (without an author) '
                                                 'at the start or end of your bibliography '
                                                 'when being processed.')


    parser.add_argument('bibfile', type=str, metavar='bibliography',
                            help='Path to your bibliography file.')

    parser.add_argument('placement', type=str,
                        choices=['top', 'bottom'],
                        help='Where you want your Misc entries to appear '
                             ' in your bibligraphy.')

    options = parser.parse_args()
    sys.exit(main(options.bibfile, options.placement))
