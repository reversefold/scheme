

class SchemeParser(object):
    class token(object):
        pass

    class tuple(token):
        symbol = '('

        def __init__(self, value):
            self.value = value

        def eval(self):
            return self.value[0].eval(*[token.eval() for token in self.value[1:]])

        def __str__(self):
            return '(%s)' % ' '.join([str(val) for val in self.value])

        def __getattr__(self, key):
            return self.value[key]

    class literal(token):
        symbol = "'"

        def __init__(self, value):
            self.value = value

        def eval(self):
            return self.value

        def __str__(self):
            return "'%s" % self.value

    class plus(token):
        symbol = '+'

        def eval(self, a, b):
            return a + b

        def __str__(self):
            return '+'

    class minus(token):
        symbol = '-'

        def eval(self, a, b):
            return a - b

        def __str__(self):
            return '-'

    class car(token):
        symbol = 'car'

        def eval(self, l):
            return l.value[0]

        def __str__(self):
            return 'car'

    class cdr(token):
        symbol = 'cdr'

        def eval(self, l):
            return SchemeParser.tuple(l.value[1:])

        def __str__(self):
            return 'cdr'

    class cons(token):
        symbol = 'cons'

        def eval(self, a, b):
            return SchemeParser.tuple([ a ] + b.value)

        def __str__(self):
            return 'cons'

    _map = None

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
            return SchemeParser.tuple(l)

        elif c == "'":
            self.txt = self.txt[1:]
            return SchemeParser.literal(self.parse(literal=True))

        i = 0
        while i < len(self.txt) and self.txt[i] not in SchemeParser._white and self.txt[i] != ')':
            i += 1

        value = self.txt[:i]
        self.txt = self.txt[i:]

        if literal:
            return value

        if value[0] >= '0' and value[0] <= '9':
            return SchemeParser.literal(int(value))

        return SchemeParser._map[value]()

SchemeParser._map = dict(
    [(cls.symbol, cls) for cls in
     [getattr(SchemeParser, name) for name in SchemeParser.__dict__]
     if isinstance(cls, type) and issubclass(cls, SchemeParser.token) and 'symbol' in cls.__dict__])

class Scheme(object):
    def __init__(self, arg):
        if isinstance(arg, SchemeParser.token):
            self.token = arg
        elif isinstance(arg, SchemeParser):
            self.token = arg.parse()
        else:
            self.token = SchemeParser(arg).parse()
    
    def eval(self):
        return self.token.eval()

#    def _resolve(self, tokens):
#        r = []
#        for t in tokens:
#            if isinstance(t, list):
#                r.append(self._eval(t))
#            else:
#                r.append(t)
#        return r

for expr in [
        '(+ 1 2)',
        '(- 3 2)',
        "(car '(1 2 3))",
        "(cdr '(1 2 3))",
        "(cons 3 '(1 2))",
        "(cons (+ 1 (- 3 (+ 15 34))) '(4 5))",
        ]:
    print "Input: %s" % expr
    token = SchemeParser(expr).parse()
    print "Token: %s" % token
    s = Scheme(token)
    print "Value: %s\n" % s.eval()
