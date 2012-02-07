from scheme.parser.token import base

class char_t(base.token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self

    def ceval(self, k, env):
        return base.Bounce(k, self)

    def __str__(self):
        return '#\\%s' % (self.value,)

    def __eq__(self, b):
        return base.boolean(self.value == b.value)

    def __ne__(self, b):
        return base.boolean(self.value != b.value)

    def __lt__(self, b):
        return base.boolean(self.value < b.value)

    def __gt__(self, b):
        return base.boolean(self.value > b.value)

    def __le__(self, b):
        return base.boolean(self.value <= b.value)

    def __ge__(self, b):
        return base.boolean(self.value >= b.value)

    def lower(self):
        return char_t(self.value.lower())

    def upper(self):
        return char_t(self.value.upper())

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
        return a == b

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a == b)

class char_lt(base.token):
    symbol = 'char<?'

    @staticmethod
    def eval(env, a, b):
        return a < b

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a < b)

class char_gt(base.token):
    symbol = 'char>?'

    @staticmethod
    def eval(env, a, b):
        return a > b

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a > b)

class char_le(base.token):
    symbol = 'char<=?'

    @staticmethod
    def eval(env, a, b):
        return a <= b

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a <= b)

class char_ge(base.token):
    symbol = 'char>=?'

    @staticmethod
    def eval(env, a, b):
        return a >= b

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a >= b)

class char_ci_eq(base.token):
    symbol = 'char-ci=?'

    @staticmethod
    def eval(env, a, b):
        return a.lower() == b.lower()

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a.lower() == b.lower())

class char_ci_lt(base.token):
    symbol = 'char-ci<?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() < b.value.lower()

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a.lower() < b.lower())

class char_ci_gt(base.token):
    symbol = 'char-ci>?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() > b.value.lower()

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a.lower() > b.lower())

class char_ci_le(base.token):
    symbol = 'char-ci<=?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() <= b.value.lower()

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a.lower() <= b.lower())

class char_ci_ge(base.token):
    symbol = 'char-ci>=?'

    @staticmethod
    def eval(env, a, b):
        return a.value.lower() >= b.value.lower()

    @staticmethod
    def ceval(k, env, a, b):
        return base.Bounce(k, a.lower() >= b.lower())
