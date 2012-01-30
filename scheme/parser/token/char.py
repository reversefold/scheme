from scheme.parser.token import base

class char_t(base.token):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self

    def __str__(self):
        return '#\\%s' % (self.value,)
