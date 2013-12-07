import math

from scheme.parser.token import base

class plus(base.token):
    symbol = '+'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) + b.eval(env))

    @staticmethod
    def ceval(k, env, a, b):
        def with_a(a_val):
            def with_b(b_val):
                return base.Bounce(k, base.number(a_val + b_val))
            return base.Bounce(b.ceval, with_b, env)
        return base.Bounce(a.ceval, with_a, env)

class minus(base.token):
    symbol = '-'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) - b.eval(env))

    @staticmethod
    def ceval(k, env, a, b):
        def with_a(a_val):
            def with_b(b_val):
                return base.Bounce(k, base.number(a_val - b_val))
            return base.Bounce(b.ceval, with_b, env)
        return base.Bounce(a.ceval, with_a, env)

class mult(base.token):
    symbol = '*'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) * b.eval(env))

    @staticmethod
    def ceval(k, env, a, b):
        def with_a(a_val):
            def with_b(b_val):
                return base.Bounce(k, base.number(a_val * b_val))
            return base.Bounce(b.ceval, with_b, env)
        return base.Bounce(a.ceval, with_a, env)

class div(base.token):
    symbol = '/'

    @staticmethod
    def eval(env, a, b):
        return base.number(a.eval(env) / b.eval(env))

    @staticmethod
    def ceval(k, env, a, b):
        def with_a(a_val):
            def with_b(b_val):
                return base.Bounce(k, base.number(a_val / b_val))
            return base.Bounce(b.ceval, with_b, env)
        return base.Bounce(a.ceval, with_a, env)

class gt(base.token):
    symbol = '>'

    @staticmethod
    def eval(env, a, b):
        return base.boolean(a.eval(env) > b.eval(env))

    @staticmethod
    def ceval(k, env, a, b):
        def with_a(a_val):
            def with_b(b_val):
                return base.Bounce(k, base.boolean(a_val > b_val))
            return base.Bounce(b.ceval, with_b, env)
        return base.Bounce(a.ceval, with_a, env)

class lt(base.token):
    symbol = '<'

    @staticmethod
    def eval(env, a, b):
        return base.boolean(a.eval(env) < b.eval(env))

    @staticmethod
    def ceval(k, env, a, b):
        def with_a(a_val):
            def with_b(b_val):
                return base.Bounce(k, base.boolean(a_val < b_val))
            return base.Bounce(b.ceval, with_b, env)
        return base.Bounce(a.ceval, with_a, env)

class eq_op(base.token):
    symbol = '='

    @staticmethod
    def eval(env, a, b):
        return base.boolean(a.eval(env) == b.eval(env))

    @staticmethod
    def ceval(k, env, a, b):
        def with_a(a_val):
            def with_b(b_val):
                return base.Bounce(k, base.boolean(a_val == b_val))
            return base.Bounce(b.ceval, with_b, env)
        return base.Bounce(a.ceval, with_a, env)


class ceiling_p(base.token):
    symbol = 'ceiling'

    @staticmethod
    def eval(env, v):
        return base.number(math.ceil(v.eval(env).value))

    @staticmethod
    def ceval(k, env, v):
        def with_val(val):
            return base.Bounce(k, base.number(math.ceil(val.value)))
        return base.Bounce(v.ceval, with_val, env)


class floor_p(base.token):
    symbol = 'floor'

    @staticmethod
    def eval(env, v):
        return base.number(math.floor(v.eval(env).value))

    @staticmethod
    def ceval(k, env, v):
        def with_val(val):
            return base.Bounce(k, base.number(math.floor(val.value)))
        return base.Bounce(v.ceval, with_val, env)
