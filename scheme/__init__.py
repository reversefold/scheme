from scheme.parser import SchemeParser
from scheme.parser import token

class Scheme(object):
    def __init__(self, arg):
        if isinstance(arg, token.token):
            self.token = arg
        elif isinstance(arg, SchemeParser):
            self.token = arg.parse()
        else:
            self.token = SchemeParser(arg).parse()

    def eval(self):
        return self.token.eval()
