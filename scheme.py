

class SchemeParser(object):
    class token(object):
        def __init__(self, token):
            self.token = token

    class tuple(token):
        symbol = '('

        def eval(self):
            return self.token[0](*[token.eval() for token in self.token[1:]])

    class literal(token):
        symbol = "'"

        def eval(self):
            return self.token

    class plus(token):
        symbol = '+'

        def eval(self):
            return self.token[0] + self.token[1]

    _map = dict()

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

    def parse(self):
        self._eat_white()
        l = []
        while self.txt:
            c = self.txt[0]
            self.txt = self.txt[1:]
            if c == '(':
                token = self.parse()

            elif c == ')':
                break

            elif c == "'":
                # literal
                # token = self.literal?
                pass

            elif c >= '0' and c <= '9':
                n = [c]
                i = 0
                while self.txt[i] >= '0' and self.txt[i] <= '9':
                    n.append(self.txt[i])
                    i += 1
                self.txt = self.txt[len(n) - 1:]
                if self.txt[0] not in (' ', ')'):
                    raise Exception("Unexpected char %r after number chars %r" % (self.txt[0], ''.join(n)))
                token = int(''.join(n))

            elif c == ' ':
                continue

            elif c in Scheme._funcs:
                token = Scheme._funcs[c]

            else:
                raise Exception("Unknown char %r" % c)

            l.append(token)

        return l

class Scheme(object):
    _funcs = {
        '+':    'plus',
        '-':    'minus',
        'car':  'car',
        'cdr':  'cdr',
        'cons': 'cons',
    }

    def __init__(self, arg):
        if isinstance(arg, list):
            self.tokens = arg
        elif isinstance(arg, SchemeParser):
            self.tokens = arg.parse()[0]
        else:
            self.tokens = SchemeParser(arg).parse()[0]
    
    def eval(self):
        return self._eval(self.tokens)

    def _eval(self, tokens):
        return tokens[0](*self._resolve(tokens[1:]))

    def _resolve(self, tokens):
        r = []
        for t in tokens:
            if isinstance(t, list):
                r.append(self._eval(t))
            else:
                r.append(t)
        return r


    @staticmethod
    def plus(a, b):
        return a + b

    @staticmethod
    def minus(a, b):
        return a - b

    @staticmethod
    def car(l):
        return l[0]

    @staticmethod
    def cdr(l):
        return l[1:]

    @staticmethod
    def cons(a, b):
        return [ a ] + b

for k in Scheme._funcs:
    Scheme._funcs[k] = getattr(Scheme, Scheme._funcs[k])

print Scheme('(+ 1 2)').eval()
print Scheme('(- 3 2)').eval()
print Scheme("(cons (+ 1 (- 3 (+ 15 34))) '(4 5))").eval()
