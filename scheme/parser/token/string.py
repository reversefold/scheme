from scheme.parser.token import base, char

class string_t(base.token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self

    def __str__(self):
        return '"%s"' % (self.value.replace('"', '__BACKSLASH__"').replace('\\', '\\\\').replace('__BACKSLASH__', '\\'),)

    def __getitem__(self, key):
        return char.char_t(self.value[key])

    def __len__(self):
        return len(self.value)

class string_f(base.token):
    symbol = 'string'

    @staticmethod
    def eval(env, *lst):
        return string_t(''.join([c.eval(env).value for c in lst]))

class string_eq(base.token):
    symbol = 'string=?'

    @staticmethod
    def eval(env, a, b):
        return a == b
