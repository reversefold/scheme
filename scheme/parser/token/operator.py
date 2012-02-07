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
