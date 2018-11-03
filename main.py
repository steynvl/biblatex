#!/usr/bin/env python3

import sys
import re
from entry import Entry

misc_entries = re.compile(r'@misc\{[^,]+,')

def read_file(path: str) -> str:
    with open(path, 'r') as f:
        return ''.join(f.readlines())


def get_misc_entries(contents: str):
    for match in misc_entries.finditer(contents):
        # start and end of match
        start, end = match.start(), match.end()
        # contains content for biblatex entry
        entry_content = [contents[start:end]]

        num_parens = 1
        index = end + 1
        while num_parens > 0:
            char = contents[index]
            if char == '{':
                num_parens += 1
            elif char == '}':
                num_parens -= 1
            entry_content.append(char)
            index += 1

        yield Entry(start, index, ''.join(entry_content))


def main(bibfile, placement):
    # read bibliography file into memory
    contents = read_file(bibfile)

    # get list of misc entries in bibliography file
    entries = list(get_misc_entries(contents))

    for entry in entries:
        print(entry)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: ./main <bibliography.bib> <top|bottom>')
    elif not sys.argv[1].endswith('.bib'):
        print('Bibliography file must be a .bib extension')
    elif sys.argv[2] not in ['top', 'bottom']:
        print('Second argument must be "top" or "bottom", depending on' +
              ' where you want to put your Misc entries.')
    else:
        sys.exit(main(sys.argv[1], sys.argv[2]))
