class environment(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.cache = dict()
        self.dict = dict()

    def __getitem__(self, key):
        if key in self.cache:
            return self.cache[key]

        if key in self.dict:
            val = self.dict[key]
        elif self.parent is None:
            raise KeyError("key %r not in environment" % key)
        else:
            val = self.parent[key]
        self.cache[key] = val
        return val

    def __setitem__(self, key, value):
        if key in self.cache:
            del self.cache[key]

        self.dict[key] = value

    def __contains__(self, item):
        return item in self.dict

    def __str__(self):
        return str(self.flattened())

    def flattened(self):
        if self.parent is None:
            return self.dict
        return dict(self.parent.items() + self.dict.items())

    def items(self):
        return self.flattened().items()
