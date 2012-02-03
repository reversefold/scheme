from scheme.parser.token import base

class plus(base.token):
    symbol = '+'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) + b.eval(env))

class minus(base.token):
    symbol = '-'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) - b.eval(env))

class mult(base.token):
    symbol = '*'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) * b.eval(env))

class div(base.token):
    symbol = '/'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) / b.eval(env))

class gt(base.token):
    symbol = '>'

    @staticmethod
    def eval(env, a, b):
        return base.boolean(a.eval(env) > b.eval(env))

class lt(base.token):
    symbol = '<'

    @staticmethod
    def eval(env, a, b):
        return base.boolean(a.eval(env) < b.eval(env))

class eq_op(base.token):
    symbol = '='

    @staticmethod
    def eval(env, a, b):
        return base.boolean(a.eval(env) == b.eval(env))
