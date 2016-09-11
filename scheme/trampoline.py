# Borrowed from Davy Wybiral at http://knol.google.com/k/davy-wybiral/trampolining-in-python/23oi5sywhe2tp/2#


class Bounce(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        # self.__call__ = lambda: func(*args, **kwargs)

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


class CountedBounce(Bounce):
    i = 0
    c = 0

    def __init__(self, func, *args, **kwargs):
        CountedBounce.i += 1
        super(CountedBounce, self).__init__(func, *args, **kwargs)

    def __call__(self):
        CountedBounce.c += 1
        # print "%r %r %r" % (self.func, self.args, self.kwargs)
        self.output()
        return super(CountedBounce, self).__call__()

    @classmethod
    def output(cls, force=False):
        if force or cls.c % 100000 == 0:
            print "CountedBounce %i %i" % (cls.i, cls.c)


# Bounce = CountedBounce


def trampoline(value):
    while isinstance(value, Bounce):
        value = value()
    if Bounce is CountedBounce:
        CountedBounce.output(True)
    return value
