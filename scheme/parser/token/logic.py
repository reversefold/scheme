from scheme.parser.token import base, equivalency

class and_t(base.token):
    symbol = 'and'

    def eval(self, env, *l):
        for p in l:
            v = p.eval(env)
            if not v:
                return v
        else:
            return base.boolean(True)
        return v

class or_t(base.token):
    symbol = 'or'

    def eval(self, env, *l):
        for p in l:
            v = p.eval(env)
            if v:
                return v
        else:
            return base.boolean(False)
        return v

class if_t(base.token):
    symbol = 'if'

    def eval(self, env, cond, t, f):
        if cond.eval(env):
            return t.eval(env)
        else:
            return f.eval(env)

class cond(base.token):
    symbol = 'cond'

    def eval(self, env, *l):
        # TODO: what if len(l) == 0?
        for i in l:
            # TODO: what if len(i) == 0?
            if i[0].eval(env):
                # TODO: what if len(i[1:]) == 0?
                # eval remaining and return last value
                return [j.eval(env) for j in i[1:]][-1]

class else_t(base.token):
    symbol = 'else'

    def eval(self, env):
        return True

class case(base.token):
    symbol = 'case'

    def eval(self, env, *l):
        val = l[0].eval(env)
        # TODO: what if len(l[1:]) == 0?
        for i in l[1:]:
            if isinstance(i[0], else_t) or isinstance(i[0], base.label) and isinstance(i[0].token(env), else_t):
                found = True
            else:
                found = False
                for v in i[0]:
                    if equivalency.eqv.eval(env, val, v):
                        found = True
                        break
            if found:
                # TODO: what if len(i[1:]) == 0?
                # eval remaining and return last value
                return [j.eval(env) for j in i[1:]][-1]
        # TODO: what if no condition is satisfied? (unspecified?)
