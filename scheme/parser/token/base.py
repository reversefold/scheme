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
        return '(%s)' % ' '.join([str(val) for val in self.value])

    def __getitem__(self, key):
        return self.value[key]

class literal(token):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return "'%s" % self.value

class int_t(literal):
    def __init__(self, value):
        self.value = int(value)

    def __eq__(self, r):
        return r.__class__ is int_t and self.value == r.value

    def __ne__(self, r):
        return r.__class__ is not int_t or self.value != r.value

    def __str__(self):
        return str(self.value)

class boolean(token):
    def __init__(self, value):
        if value is True:
            value = '#t'
        elif value is False:
            value = '#f'
        self.value = value

    def eval(self):
        return self

    def __nonzero__(self):
        return self.value != '#f'

    def __str__(self):
        return self.value

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
