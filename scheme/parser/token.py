class token(object):
    def __str__(self):
        return self.__class__.symbol

    def bool(self):
        return True

class tuple(token):
    symbol = '('

    def __init__(self, value):
        self.value = value

    def eval(self):
        #return self.value[0].eval(*[token.eval() for token in self.value[1:]])
        return self.value[0].eval(*self.value[1:])

    def __str__(self):
        return '(%s)' % ' '.join([str(val) for val in self.value])

    def __getitem__(self, key):
        return self.value[key]

class literal(token):
    symbol = "'"

    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return "'%s" % self.value

class plus(token):
    symbol = '+'

    def eval(self, a, b):
        return literal(a.eval().value + b.eval().value)

class minus(token):
    symbol = '-'

    def eval(self, a, b):
        return literal(a.eval().value - b.eval().value)

class car(token):
    symbol = 'car'

    def eval(self, l):
        return l.value[0]

class cdr(token):
    symbol = 'cdr'

    def eval(self, l):
        return tuple(l.value[1:])

class cons(token):
    symbol = 'cons'

    def eval(self, a, b):
        return tuple([ a.eval() ] + (b.value.value if isinstance(b.value, tuple) else b.value))

class boolean(token):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def bool(self):
        return self.value != '#f'

    def __str__(self):
        return self.value

class _if(token):
    symbol = 'if'

    def eval(self, cond, t, f):
        if cond.eval().bool():
            return t
        else:
            return f

_map = dict(
    [(cls.symbol, cls) for cls in locals().values()
     if isinstance(cls, type) and issubclass(cls, token) and 'symbol' in cls.__dict__])
