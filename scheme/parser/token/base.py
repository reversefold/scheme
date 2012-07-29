from __future__ import division

import fractions

from scheme.trampoline import Bounce

class token(object):
    def __str__(self):
        return self.__class__.symbol

    def __nonzero__(self):
        return True

class tuple(token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value[0].eval(env).eval(env, *self.value[1:])

    def ceval(self, k, env):
        def with_func(f):
            return Bounce(f.ceval, k, env, *self.value[1:])
#        print self
        return Bounce(self.value[0].ceval, with_func, env)

    def __str__(self):
        return '(%s)' % (' '.join([str(val) for val in self.value]),)

    # Proxy methods
    def __getitem__(self, key):
        ret = self.value[key]
        if isinstance(ret, list):
            ret = tuple(ret)
        return ret

    def __len__(self):
        return len(self.value)

    def __add__(self, r):
        return tuple(self.value + r.value)


def resolve_list(k, env, lst):
    if not lst:
        return Bounce(k, tuple([]))
    def with_val(v):
        def with_resolved(r):
            return Bounce(k, tuple([v]) + r)
        return Bounce(resolve_list, with_resolved, env, lst[1:])
    return Bounce(lst[0].ceval, with_val, env)

def return_last(k, env, l):
    def with_val(v):
        if len(l) == 1:
            return Bounce(k, v)
        return Bounce(return_last, k, env, l[1:])
    return Bounce(l[0].ceval, with_val, env)


class quoted(token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

    def ceval(self, k, env):
        return Bounce(k, self.value)

    def __str__(self):
        if isinstance(self.value, number) or isinstance(self.value, boolean):
            return str(self.value)
        return "'%s" % (str(self.value),)

class quote(token):
    symbol = 'quote'

    @staticmethod
    def eval(env, l):
        return quoted(l)

    @staticmethod
    def ceval(k, env, l):
        return Bounce(k, quoted(l))

class number(token):
    def __init__(self, value):
        self.value = fractions.Fraction(value)

    def eval(self, env):
        return self

    def ceval(self, k, env):
        return Bounce(k, self)

    def __eq__(self, r):
        return r.__class__ is number and self.value == r.value

    def __ne__(self, r):
        return r.__class__ is not number or self.value != r.value

    # Proxy methods
    def __add__(self, r):
        return self.value.__add__(r.value)

    def __sub__(self, r):
        return self.value.__sub__(r.value)

    def __mul__(self, r):
        return self.value.__mul__(r.value)

    def __div__(self, r):
        return self.value.__div__(r.value)

    def __truediv__(self, r):
        return self.value.__truediv__(r.value)

    def __gt__(self, r):
        return self.value.__gt__(r.value)

    def __lt__(self, r):
        return self.value.__lt__(r.value)

    def __ge__(self, r):
        return self.value.__ge__(r.value)

    def __le__(self, r):
        return self.value.__le__(r.value)

    def __str__(self):
        return str(self.value)

class boolean(token):
    def __init__(self, value):
        if value == '#t':
            value = True
        elif value == '#f':
            value = False
        self.value = value

    def eval(self, env):
        return self

    def ceval(self, k, env):
        return Bounce(k, self)

    def __nonzero__(self):
        return self.value

    def __str__(self):
        return '#t' if self.value else '#f'

class label(token):
    def __init__(self, value):
        self.value = value

    def token(self, env):
        return env[self.value]

    def ctoken(self, k, env):
        return Bounce(env.cget, k, self.value)

    def eval(self, env):
        return self.token(env)

    def ceval(self, k, env):
        return Bounce(self.ctoken, k, env)

    def __str__(self):
        return self.value
