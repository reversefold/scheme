from scheme.parser.token import base

class char_t(base.token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self

    def __str__(self):
        return '#\\%s' % (self.value,)

class named_char(char_t):
    def __init__(self, name):
        self.name = name
        super(named_char, self).__init__(named_char._map[self.name])

    def __str__(self):
        return '#\\%s' % (self.name,)

    _map = {
        'space': ' '
    }

class char_eq(base.token):
    symbol = 'char=?'

    @staticmethod
    def eval(env, a, b):
        return a.value == b.value

class char_lt(base.token):
    symbol = 'char<?'

    @staticmethod
    def eval(env, a, b):
        return a.value < b.value

class char_gt(base.token):
    symbol = 'char>?'

    @staticmethod
    def eval(env, a, b):
        return a.value > b.value

class char_le(base.token):
    symbol = 'char<=?'

    @staticmethod
    def eval(env, a, b):
        return a.value <= b.value

class char_ge(base.token):
    symbol = 'char>=?'

    @staticmethod
    def eval(env, a, b):
        return a.value >= b.value

class char_ci_eq(base.token):
    symbol = 'char-ci=?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() == b.value.lower()

class char_ci_lt(base.token):
    symbol = 'char-ci<?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() < b.value.lower()

class char_ci_gt(base.token):
    symbol = 'char-ci>?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() > b.value.lower()

class char_ci_le(base.token):
    symbol = 'char-ci<=?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() <= b.value.lower()

class char_ci_ge(base.token):
    symbol = 'char-ci>=?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() >= b.value.lower()
