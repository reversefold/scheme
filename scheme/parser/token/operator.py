from scheme.parser.token import base

class plus(base.token):
    symbol = '+'

    def eval(self, a, b):
        return base.number(a.eval() + b.eval())

class minus(base.token):
    symbol = '-'

    def eval(self, a, b):
        return base.number(a.eval() - b.eval())

class mult(base.token):
    symbol = '*'

    def eval(self, a, b):
        return base.number(a.eval() * b.eval())

class div(base.token):
    symbol = '/'

    def eval(self, a, b):
        return base.number(a.eval() / b.eval())

class gt(base.token):
    symbol = '>'

    def eval(self, a, b):
        return base.boolean(a.eval() > b.eval())

class lt(base.token):
    symbol = '<'

    def eval(self, a, b):
        return base.boolean(a.eval() < b.eval())
