class Entry:

    def __init__(self, start, end, text):
        self._start = start
        self._end = end
        self._text = text

    def __str__(self):
        return '({}, {}):\n{}'.format(self._start,
                                     self._end,
                                     self._text)
