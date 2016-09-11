from scheme.parser.token import base, equivalency


class and_t(base.token):
    symbol = 'and'

    @staticmethod
    def eval(env, *l):
        for p in l:
            v = p.eval(env)
            if not v:
                return v
        else:
            return base.boolean(True)
        return v

    @staticmethod
    def ceval(k, env, *l):
#        print l
#        print "%s" % (base.tuple(l),)
#        if not l:
#            print k
#            return base.Bounce(k, base.boolean(True))
        p = l[0]
#        ll = {'l': l[1:]}

        def with_val(v):
#            l = ll['l']
            if not v or len(l) == 1:
                return base.Bounce(k, v)
#            p = l[0]
#            ll['l'] = l[1:]
#            return base.Bounce(p.ceval, with_val, env)
            return base.Bounce(and_t.ceval, k, env, *l[1:])
        return base.Bounce(p.ceval, with_val, env)


class or_t(base.token):
    symbol = 'or'

    @staticmethod
    def eval(env, *l):
        for p in l:
            v = p.eval(env)
            if v:
                return v
        else:
            return base.boolean(False)
        return v

    @staticmethod
    def ceval(k, env, *l):
        p = l[0]

        def with_val(v):
            if v or len(l) == 1:
                return base.Bounce(k, v)
            return base.Bounce(or_t.ceval, k, env, *l[1:])
        return base.Bounce(p.ceval, with_val, env)


class if_t(base.token):
    symbol = 'if'

    @staticmethod
    def eval(env, cond, t, f):
        if cond.eval(env):
            return t.eval(env)
        else:
            return f.eval(env)

    @staticmethod
    def ceval(k, env, cond, t, f):
        def with_val(v):
            if v:
                return base.Bounce(t.ceval, k, env)
            else:
                return base.Bounce(f.ceval, k, env)
        return base.Bounce(cond.ceval, with_val, env)


class cond(base.token):
    symbol = 'cond'

    @staticmethod
    def eval(env, *l):
        # TODO: what if len(l) == 0?
        for i in l:
            # TODO: what if len(i) == 0?
            if i[0].eval(env):
                # TODO: what if len(i[1:]) == 0?
                # eval remaining and return last value
                return [j.eval(env) for j in i[1:]][-1]

    @staticmethod
    def ceval(k, env, *l):
        p = l[0][0]

        def with_val(v):
            if v:
                if len(l[0]) == 1:
                    return base.Bounce(k, v)
                return base.Bounce(base.return_last, k, env, l[0][1:])
#                loop through l[0][1:] and return last
            if len(l) == 1:
                # unspecified
                return base.Bounce(k, None)
            return base.Bounce(cond.ceval, k, env, *l[1:])
        return base.Bounce(p.ceval, with_val, env)


class else_t(base.token):
    symbol = 'else'

#    @staticmethod
#    def eval(env):
#        return True


class case(base.token):
    symbol = 'case'

    @staticmethod
    def eval(env, *l):
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

    @staticmethod
    def case_ceval(k, env, v, l):
        if not l:
            return base.Bounce(k, None)
        i = l[0]
        if isinstance(i[0], else_t):
            return base.Bounce(base.return_last, k, env, i[1:])
        if isinstance(i[0], base.label):
            def with_token(token):
                if isinstance(token, else_t):
                    return base.Bounce(base.return_last, k, env, i[1:])
                else:
                    return base.Bounce(case.case_ceval, k, env, v, l[1:])
            return base.Bounce(i[0].ctoken, with_token, env)
        for iv in i[0]:
            if equivalency.eqv.eval(env, v, iv):
                return base.Bounce(base.return_last, k, env, i[1:])
        return base.Bounce(case.case_ceval, k, env, v, l[1:])

    @staticmethod
    def ceval(k, env, *l):
        p = l[0]

        def with_val(v):
            return base.Bounce(case.case_ceval, k, env, v, l[1:])
        return base.Bounce(p.ceval, with_val, env)
