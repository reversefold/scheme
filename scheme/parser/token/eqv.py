from scheme.parser.token import base

class eqv(base.token):
    symbol = 'eqv?'

    @staticmethod
    def eval(a, b):
        if a.__class__ != b.__class__:
            return base.boolean(False)
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
