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

class char_u(char_t):
    def __init__(self, num):
        super(char_u, self).__init__(unichr(num))

class named_char(char_t):
    def __init__(self, name):
        self.name = name
        super(named_char, self).__init__(named_char._map[self.name])

    def __str__(self):
        return '#\\%s' % (self.name,)

    _map = {
        'space':     ' ',
        'altmode':   chr(27),
        'backnext':  chr(31),
        'backspace': chr(8),
        'call':      chr(26),
        'linefeed':  '\n',
        'newline':   '\n',
        'page':      chr(12),
        'return':    '\r',
        'rubout':    chr(127),
        'tab':       '\t',
        'NUL':       chr(0),
        'SOH':       chr(1),
        'STX':       chr(2),
        'ETX':       chr(3),
        'EOT':       chr(4),
        'ENQ':       chr(5),
        'ACK':       chr(6),
        'BEL':       chr(7),
        'BS':        chr(8),
        'HT':        chr(9),
        'LF':        chr(10),
        'VT':        chr(11),
        'FF':        chr(12),
        'CR':        chr(13),
        'SO':        chr(14),
        'SI':        chr(15),
        'DLE':       chr(16),
        'DC1':       chr(17),
        'DC2':       chr(18),
        'DC3':       chr(19),
        'DC4':       chr(20),
        'NAK':       chr(21),
        'SYN':       chr(22),
        'ETB':       chr(23),
        'CAN':       chr(24),
        'EM':        chr(25),
        'SUB':       chr(26),
        'ESC':       chr(27),
        'FS':        chr(28),
        'GS':        chr(29),
        'RS':        chr(30),
        'US':        chr(31),
        'DEL':       chr(127),
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

class char_to_name(base.token):
    symbol = 'char->name'

    @staticmethod
    def eval(env, val):
        raise Exception("Not finished")

    @staticmethod
    def ceval(k, env, val):
        raise Exception("Not finished")

class name_to_char(base.token):
    symbol = 'name->char'

    @staticmethod
    def eval(env, val):
        # TODO: Assumption that val is a string_t
        return char_t(named_char._map[val.eval().value])

    @staticmethod
    def ceval(k, env, val):
        def with_val(v):
            # TODO: Assumption that val is a string_t
            return base.Bounce(k, v.value)
        return base.Bounce(val.ceval, with_val, env)
