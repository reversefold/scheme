from scheme.environment import environment
from scheme.parser import SchemeParser
from scheme.parser import token
from scheme.trampoline import trampoline

class Scheme(object):
    def __init__(self, arg):
        if isinstance(arg, token.token):
            self.token = arg
        else:
            if isinstance(arg, SchemeParser):
                parser = arg
            else:
                parser = SchemeParser(arg)
            self.token = trampoline(parser.cparse(lambda x: x))
#            self.token = parser.parse()

    def eval(self):
        env = environment()
        return self.token.eval(env)

    def ceval(self):
        env = environment()
        return trampoline(self.token.ceval(lambda x: x, env))
