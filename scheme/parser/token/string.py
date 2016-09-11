from scheme.parser.token import base, char


class string_t(base.token):
    def __init__(self, value):
        self.value = value

    def eval(self, env):
        return self

    def ceval(self, k, env):
        return base.Bounce(k, self)

    def __str__(self):
        return '"%s"' % (self.value.replace('"', '__BACKSLASH__"').replace('\\', '\\\\').replace('__BACKSLASH__', '\\'),)

    def __getitem__(self, key):
        return char.char_t(self.value[key])

    def __len__(self):
        return len(self.value)

    def __eq__(self, b):
        # TODO: assumption that b is a string_t instance
        return base.boolean(self.value == b.value)


class string_f(base.token):
    symbol = 'string'

    @staticmethod
    def eval(env, *lst):
        return string_t(''.join([c.eval(env).value for c in lst]))

    @staticmethod
    def ceval(k, env, *lst):
        def with_val(v):
            # TODO: assumption that i is a char_t
            return base.Bounce(k, string_t(''.join([i.value for i in v])))
        return base.Bounce(base.resolve_list, with_val, env, lst)


class string_eq(base.token):
    symbol = 'string=?'

    @staticmethod
    def eval(env, a, b):
        # TODO: assumption that a and b are string_t instances
        return a == b

    @staticmethod
    def ceval(k, env, a, b):
        # TODO: assumption that a and b are string_t instances
        return base.Bounce(k, a == b)
