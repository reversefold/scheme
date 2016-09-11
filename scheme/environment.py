class environment(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.cache = dict()
        self.dict = dict()
        self._flattened = None

    def __getitem__(self, key):
        if key in self.cache:
            return self.cache[key]

        if key in self.dict:
            val = self.dict[key]
        elif self.parent is None:
            # TODO: no env in ()?
            import scheme.parser.token
            return scheme.parser.token._map[key]()
#            raise KeyError("key %r not in environment" % key)
        else:
            val = self.parent[key]
        self.cache[key] = val
        return val

    def __setitem__(self, key, value):
        if key in self.cache:
            del self.cache[key]

        self._flattened = None

        self.dict[key] = value

    def __contains__(self, item):
        return item in self.cache or item in self.dict or (self.parent and item in self.parent)

    def __str__(self):
        return str(self.flattened())

    def flattened(self):
        if self.parent is None:
            return self.dict
        if not self._flattened:
            self._flattened = dict(self.parent.items() + self.dict.items())
        return self._flattened

    def cflattened(self, k):
        from scheme.parser.token import base
        if self.parent is None:
            return base.Bounce(k, self.dict)
        # TODO: This causes an error ....
        # if self._flattened:
        #    return base.Bounce(k, self._flattened)

        def with_flattened_parent(v):
            self._flattened = dict(v.items() + self.dict.items())
            return base.Bounce(k, self._flattened)
        return base.Bounce(self.parent.cflattened, with_flattened_parent)

    def items(self):
        return self.flattened().items()

    def cget(self, k, key):
        from scheme.parser.token import base
        if key in self.dict:
            return base.Bounce(k, self.dict[key])
        if self.parent:
            return base.Bounce(self.parent.cget, k, key)
        import scheme.parser.token
        return base.Bounce(k, scheme.parser.token._map[key]())
