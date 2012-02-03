from scheme.parser.token import base

class isnull(base.token):
    symbol = 'null?'

    def eval(self, env, l):
        return base.boolean(len(l.eval(env)) == 0)

class length(base.token):
    symbol = 'length'

    def eval(self, env, l):
        return base.number(len(l.eval(env)))

class car(base.token):
    symbol = 'car'

    def eval(self, env, l):
        return l.eval(env)[0]

class rcar(base.token):
    symbol = 'rcar'

    def eval(self, env, l):
        return l.eval(env)[-1]

class cdr(base.token):
    symbol = 'cdr'

    def eval(self, env, l):
        return l.eval(env)[1:]

class cons(base.token):
    symbol = 'cons'

    def eval(self, env, a, b):
        return base.tuple([a.eval(env)]) + b.eval(env)

class list_p(base.token):
    symbol = 'list'

    def eval(self, env, *l):
        return base.tuple([i.eval(env) for i in l])
