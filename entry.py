class Entry:
    """
    Represents an entry in a LaTeX bib file
    """

    def __init__(self, start, end, text):
        self.__start = start
        self.__end = end
        self.__text = text

    @property
    def start(self):
        return self.__start

    @property
    def end(self):
        return self.__end

    @property
    def text(self):
        return self.__text

    def __str__(self):
        return '({}, {}):\n{}'.format(self.start,
                                      self.end,
                                      self.text)
