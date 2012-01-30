from scheme.parser.token import base

class string_t(base.token):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return self.value

class string_f(base.token):
    symbol = 'string'

    def eval(self, *l):
        return string_t(''.join(l))
