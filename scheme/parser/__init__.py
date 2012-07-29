from scheme.parser import token
from scheme.trampoline import Bounce

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
        if i != 0:
            self.txt = self.txt[i:]

    def parse(self):
        """
        Parses the txt passed into __init__.

        Parses a single token (including subtokens) at a time, calls itself recursively.
        """

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
            return token.quoted(self.parse())

        if self.txt[0] in self._map:
            return getattr(self, SchemeParser._map[self.txt[0]])()

        value = self._parse_value()

        return token.label(value)

    def _clist(self, k):
        # needed in case there is whitespace before the )
        self._eat_white()
        if self.txt[0] == ')':
            self.txt = self.txt[1:]
            return Bounce(k, token.tuple([]))
        def with_val(v):
            def with_list(l):
                return Bounce(k, token.tuple([v]) + l)
            return Bounce(self._clist, with_list)
        return Bounce(self.cparse, with_val)

    def cparse(self, k):
        """
        Parses the txt passed into __init__.

        Parses a single token (including subtokens) at a time, calls itself recursively.
        """

        self._eat_white()
        c = self.txt[0]
        if c == '(':
            self.txt = self.txt[1:]
            return Bounce(self._clist, k)

        elif c == "'":
            self.txt = self.txt[1:]
            def with_quoted(quoted):
                return Bounce(k, token.quoted(quoted))
            return Bounce(self.cparse, with_quoted)

        if self.txt[0] in self._map:
            return Bounce(k, getattr(self, SchemeParser._map[self.txt[0]])())

        value = self._parse_value()

        return Bounce(k, token.label(value))

    def _parse_value(self):
        i = 0
        while i < len(self.txt) and self.txt[i] not in SchemeParser._white and self.txt[i] != ')':
            i += 1

        value = self.txt[:i]
        self.txt = self.txt[i:]

        return value

    def _parse_number(self):
        value = self._parse_value()

        # TODO: support + - . inexact vs exact
        if value[0] >= '0' and value[0] <= '9':
            return token.number(value)

    def _parse_pound(self):
        value = self._parse_value()

        if value == '#t' or value == '#f':
            return token.boolean(value)

        if value[1] == '\\':
            return self._parse_char(value[2:])

        raise Exception("How do I parse %r" % (value,))

    def _parse_char(self, value):
        l = len(value)
        if l == 0:
            raise Exception("No char to char")

        if l == 1:
            return token.char_t(value)

        if value[:2] == 'U+':
            num = int(value[2:], 16)
            return token.char_u(num)

        return token.named_char(value)

    def _parse_string(self):
        value = []
        i = 1

        while i < len(self.txt) and self.txt[i] != '"':
            if self.txt[i] == '\\':
                i += 1
            value.append(self.txt[i])
            i += 1

        if i == len(self.txt):
            raise Exception('Reached end of txt while looking for "')

        i += 1

        self.txt = self.txt[i:]

        return token.string_t(''.join(value))

    _map = dict(
        [(chr(chi), '_parse_number') for chi in xrange(ord('0'), ord('9') + 1)]
        + [
            ('#', '_parse_pound'),
            ('"', '_parse_string'),
        ]
        )
