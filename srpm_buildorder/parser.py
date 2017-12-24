import re

class RecursiveDescentParser(object):
    SYMBOLS = [] # [(symbol, re.compile(pattern))]

    def __init__(self, line):
        self.line = line
        self.input = line
        self.prev_input = None
        self.sym = None
        self.val = None

    def accept(self, sym):
        if self.sym == sym:
            self.nextsym()
            return True
        return False

    def expect(self, sym):
        if self.accept(sym):
            return True
        self.parse_error([sym])

    def nextsym(self):
        self.input = self.input.strip()
        self.prev_input = self.input
        for sym, regex in self.__class__.SYMBOLS:
            m = regex.match(self.input)
            if m:
                self.sym = sym
                self.val = m.groupdict()
                self.input = self.input[m.end():]
                return
        self.error([sym for sym, _ in self.__class__.SYMBOLS])

    def error(self, expected_syms):
        expected_syms = set(expected_syms)
        regexes = [(sym, regex.pattern) for sym, regex in self.__class__.SYMBOLS if sym in expected_syms]
        raise ValueError('Parse error, expected one of: "{}", input: "{}"'.format(regexes, self.prev_input))
