from scheme.parser.token import base

class eqv(base.token):
    symbol = 'eqv?'

    @staticmethod
    def eval(a, b):
        if a.__class__ != b.__class__:
            return base.boolean(False)
        if isinstance(a, base.tuple) and isinstance(b, base.tuple) and len(a.value) == 0 and len(b.value) == 0:
            return base.boolean(True)
        if isinstance(a, base.boolean) and isinstance(b, base.boolean) and a.value == b.value:
            return base.boolean(True)
        if a != b:
            return base.boolean(False)
        return base.boolean(True)

class eq(base.token):
    symbol = 'eq?'

    @staticmethod
    def eval(a, b):
        return base.boolean(a == b)

class equal(base.token):
    symbol = 'equal?'

    @staticmethod
    def eval(a, b):
        if isinstance(base.tuple, a) and isinstance(base.tuple, b):
            if len(a) != len(b):
                return base.boolean(False)
            for i in xrange(len(a)):
                if not equal.eval(a[i], b[i]):
                    return base.boolean(False)
            return base.boolean(True)
        else:
            return eqv.eval(a, b)
