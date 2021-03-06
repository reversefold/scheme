from scheme.parser.token import base, char, string


class eqv(base.token):
    symbol = 'eqv?'

    @staticmethod
    def eval(env, a, b):
        return eqv._eval(env, a, b)
#        return eqv._eval(env, a.eval(env), b.eval(env))

    @staticmethod
    def _eval(env, a, b):
        if a.__class__ != b.__class__:
            return base.boolean(False)
        if isinstance(a, base.tuple) and isinstance(b, base.tuple) and len(a.value) == 0 and len(b.value) == 0:
            return base.boolean(True)
        if isinstance(a, base.boolean) and isinstance(b, base.boolean) and a.value == b.value:
            return base.boolean(True)
        if isinstance(a, char.char_t) and isinstance(b, char.char_t) and char.char_eq.eval(env, a, b):
            return base.boolean(True)
        if isinstance(a, base.label) and isinstance(b, base.label) and string.string_eq.eval(env, a.value, b.value):
            return base.boolean(True)
        if a != b:
            return base.boolean(False)
        return base.boolean(True)

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, eqv._eval(env, a, b))
#        def with_a_value(a_value):
#            def with_b_value(b_value):
#                return base.Bounce(k, eqv._eval(a_value, b_value))
#            return base.Bounce(b.eval, with_b_value, env)
#        return base.Bounce(a.eval, with_a_value, env)


class eq(base.token):
    symbol = 'eq?'

    @staticmethod
    def eval(env, a, b):
        return eq._eval(env, a, b)
#        return eq._eval(env, a.eval(env), b.eval(env))

    @staticmethod
    def _eval(env, a, b):
        return base.boolean(a is b)

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, eq._eval(env, a, b))
#        def with_a_value(a_value):
#            def with_b_value(b_value):
#                return base.Bounce(k, eq._eval(a_value, b_value))
#            return base.Bounce(b.eval, with_b_value, env)
#        return base.Bounce(a.eval, with_a_value, env)


class equal(base.token):
    symbol = 'equal?'

    @staticmethod
    def eval(env, a, b):
        # return equal._eval(env, a, b)
        return equal._eval(env, a.eval(env), b.eval(env))

    @staticmethod
    def _eval(env, a, b):
        if (
            isinstance(a, base.tuple) and isinstance(b, base.tuple)
            or isinstance(a, string.string_t) and isinstance(b, string.string_t)
        ):
            if len(a) != len(b):
                return base.boolean(False)
            for i in xrange(len(a)):
                if not equal.eval(env, a[i], b[i]):
                    return base.boolean(False)
            return base.boolean(True)
        else:
            return eqv.eval(env, a, b)

    @staticmethod
    def ceval(k, env, a, b):
        # return base.Bounce(k, equal._eval(env, a, b))
        def with_a_value(a_value):
            def with_b_value(b_value):
                return base.Bounce(k, equal._eval(env, a_value, b_value))
            return base.Bounce(b.ceval, with_b_value, env)
        return base.Bounce(a.ceval, with_a_value, env)
