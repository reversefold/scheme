from scheme.parser.token import base

class isnull(base.token):
    symbol = 'null?'

    @staticmethod
    def eval(env, l):
        # TODO: Assumption that l is a tuple
        return base.boolean(len(l.eval(env)) == 0)

    @staticmethod
    def ceval(f, env, l):
        # TODO: Assumption that l is a tuple
        def with_val(v):
            return base.Bounce(f, base.boolean(len(v) == 0))
        return base.Bounce(l.ceval, with_val, env)

class length(base.token):
    symbol = 'length'

    @staticmethod
    def eval(env, l):
        return base.number(len(l.eval(env)))

    @staticmethod
    def ceval(k, env, l):
        def with_val(val):
            return base.Bounce(k, base.number(len(val)))
        return base.Bounce(l.ceval, with_val, env)

class car(base.token):
    symbol = 'car'

    @staticmethod
    def eval(env, l):
        return l.eval(env)[0]

    @staticmethod
    def ceval(k, env, l):
        def with_val(val):
            return base.Bounce(k, val[0])
        return base.Bounce(l.ceval, with_val, env)

class cdr(base.token):
    symbol = 'cdr'

    @staticmethod
    def eval(env, l):
        return l.eval(env)[1:]

    @staticmethod
    def ceval(k, env, l):
        def with_val(val):
            return base.Bounce(k, val[1:])
        return base.Bounce(l.ceval, with_val, env)

class cons(base.token):
    symbol = 'cons'

    @staticmethod
    def eval(env, a, b):
        return base.tuple([a.eval(env)]) + b.eval(env)

    @staticmethod
    def ceval(k, env, a, b):
        def with_aval(a_val):
            def with_bval(b_val):
                return base.Bounce(k, base.tuple([a_val]) + b_val)
            return base.Bounce(b.ceval, with_bval, env)
        return base.Bounce(a.ceval, with_aval, env)

class list_p(base.token):
    symbol = 'list'

    @staticmethod
    def eval(env, *l):
        return base.tuple([i.eval(env) for i in l])

    @staticmethod
    def ceval(k, env, *l):
        if not l:
            return base.Bounce(k, base.tuple([]))
        l = list(l)
        vals = []
        def with_val(v):
            vals.append(v)
            if l:
                return base.Bounce(l.pop(0).ceval, with_val, env)
            return base.Bounce(k, base.tuple(vals))
        return base.Bounce(l.pop(0).ceval, with_val, env)
