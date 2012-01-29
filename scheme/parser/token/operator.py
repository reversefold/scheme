from scheme.parser.token import base

class plus(base.token):
    symbol = '+'

    def eval(self, a, b):
        return base.int_t(a.eval().value + b.eval().value)

class minus(base.token):
    symbol = '-'

    def eval(self, a, b):
        return base.int_t(a.eval().value - b.eval().value)

class mult(base.token):
    symbol = '*'

    def eval(self, a, b):
        return base.int_t(a.eval().value * b.eval().value)

class div(base.token):
    symbol = '/'

    def eval(self, a, b):
        return base.int_t(a.eval().value / b.eval().value)

class gt(base.token):
    symbol = '>'

    def eval(self, a, b):
        return base.boolean(a.eval().value > b.eval().value)

class lt(base.token):
    symbol = '<'

    def eval(self, a, b):
        return base.boolean(a.eval().value < b.eval().value)
