from scheme.parser import token

class SchemeParser(object):
    _white = [
        ' ',
        '\t',
        '\n',
        '\r'
    ]

    def __init__(self, txt):
        self.txt = txt

    def _eat_white(self):
        i = 0
        while self.txt[i] in SchemeParser._white:
            i += 1
        self.txt = self.txt[i:]

    def parse(self, literal=False):
        self._eat_white()
        c = self.txt[0]
        if c == '(':
            self.txt = self.txt[1:]
            l = []
            while self.txt[0] != ')':
                l.append(self.parse())
                # needed in case there is whitespace before the )
                self._eat_white()
            self.txt = self.txt[1:]
            return token.tuple(l)

        elif c == "'":
            self.txt = self.txt[1:]
            return token.literal(self.parse(literal=True))

        i = 0
        while i < len(self.txt) and self.txt[i] not in SchemeParser._white and self.txt[i] != ')':
            i += 1

        value = self.txt[:i]
        self.txt = self.txt[i:]

        if literal:
            return value

        if value[0] >= '0' and value[0] <= '9':
            return token.int_t(value)

        if value == '#t' or value == '#f':
            return token.boolean(value)

        return token.label(value)
