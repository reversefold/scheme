from scheme.parser.token import base

class car(base.token):
    symbol = 'car'

    def eval(self, l):
        return l.value[0]

class cdr(base.token):
    symbol = 'cdr'

    def eval(self, l):
        return base.tuple(l.value[1:])

class cons(base.token):
    symbol = 'cons'

    def eval(self, a, b):
        return base.tuple([ a.eval() ] + (b.value.value if isinstance(b.value, base.tuple) else b.value))
