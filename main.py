#!/usr/bin/env python3

import argparse
import sys
import re
from entry import Entry
from typing import List, Generator

bib_entry  = re.compile(r'@[^{]+\{[^,]+,')
misc_entry = re.compile(r'@misc+\{[^,]+,')
title_val  = re.compile(r'\btitle = \{.*\},')

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return ''.join(f.readlines())


def get_entries(contents: str) -> Generator:
    for match in bib_entry.finditer(contents):
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


def transform_bib_file(source: str, entries: List[Entry],
                       placement: str, save_as: str):
    updated_entries = []
    for entry in entries:
        if misc_entry.match(entry.text) is not None:
            match = title_val.search(entry.text)
            title_text = entry.text[match.start(): match.end()]
            title_text = title_text[title_text.find('{'):-1]

            idx = entry.text.find(',')
            prefix = 'aaa-' if placement == 'top' else 'zzz-'
            key = 'key = {}{}{}'.format(title_text[0], prefix, title_text[1:])
            updated_entries.append('{}\n\t{}{}'.format(entry.text[:idx+1],
                                                       key,
                                                       entry.text[idx:]))
        else:
            updated_entries.append(entry.text)

    with open(save_as, 'w') as f:
        f.write('\n\n'.join(updated_entries))

    print('Modified bibliography saved to {}'.format(save_as))


def main(bibfile: str, placement: str):
    # read bibliography file into memory
    contents = read_file(bibfile)

    # get list of entries in bibliography file
    entries = list(get_entries(contents))

    transform_bib_file(contents, entries, placement, '{}-new.bib'.format(bibfile[:-4]))


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
