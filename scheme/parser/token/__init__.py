from base import *
from equivalency import *
from list import *
from logic import *
from operator import *

_map = dict(
    [(cls.symbol, cls) for cls in locals().values()
     if isinstance(cls, type) and issubclass(cls, token) and 'symbol' in cls.__dict__])
