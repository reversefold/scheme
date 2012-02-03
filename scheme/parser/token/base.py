from __future__ import division

import fractions

class token(object):
    def __str__(self):
        return self.__class__.symbol

    def __nonzero__(self):
        return True

class tuple(token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        ret = self.value[0].eval(env).eval(env, *self.value[1:])
#        print "tuple.eval: %s" % (self,)
#        print "ret: %s" % (ret,)
        return ret

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

class quoted(token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self.value

    def __str__(self):
        return str(self.value)

class quote(token):
    symbol = 'quote'

    def eval(self, env, l):
        return quoted(l)

class number(token):
    def __init__(self, value):
        self.value = fractions.Fraction(value)

    def eval(self, env):
        return self

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

    def __nonzero__(self):
        return self.value

    def __str__(self):
        return '#t' if self.value else '#f'

class label(token):
    def __init__(self, value):
        self.value = value

    def token(self, env):
        import scheme.parser.token
        if self.value in env:
            return env[self.value]
        # TODO: no env in ()?
        return scheme.parser.token._map[self.value]()

    def eval(self, env):
        return self.token(env)

    def __str__(self):
        return self.value
