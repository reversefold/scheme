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

    def eval(self):
        return self.value[0].eval(*self.value[1:])

    def __str__(self):
        return '(%s)' % (' '.join([str(val) for val in self.value]),)

    def __getitem__(self, key):
        return self.value[key]

class quoted(token):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return str(self.value)

class quote(token):
    symbol = 'quote'

    def eval(self, l):
        return quoted(l)

class number(token):
    def __init__(self, value):
        self.value = fractions.Fraction(value)

    def eval(self):
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

    def eval(self):
        return self

    def __nonzero__(self):
        return self.value

    def __str__(self):
        return '#t' if self.value else '#f'

class label(token):
    def __init__(self, value):
        self.value = value

    def token(self):
        import scheme.parser.token
        return scheme.parser.token._map[self.value]()

    def eval(self, *args):
        return self.token().eval(*args)

    def __str__(self):
        return self.value
