# Borrowed from Davy Wybiral at http://knol.google.com/k/davy-wybiral/trampolining-in-python/23oi5sywhe2tp/2#

class Bounce:
#    i = 0
#    c = 0

    def __init__(self, func, *args, **kwargs):
#        Bounce.i += 1
        self.func = func
        self.args = args
        self.kwargs = kwargs
        #self.__call__ = lambda: func(*args, **kwargs)

    def __call__(self):
#        Bounce.c += 1
#        print "%r %r %r" % (self.func, self.args, self.kwargs)
#        if Bounce.c % 100000 == 0:
#            print "Bounce %i %i" % (Bounce.i, Bounce.c)
        return self.func(*self.args, **self.kwargs)

def trampoline(value):
    while isinstance(value, Bounce):
        value = value()
    return value
