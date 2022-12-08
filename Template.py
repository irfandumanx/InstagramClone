class Template(type):
    def __new__(mcs, f):
        cls = type.__new__(mcs, f.__name__, (), {
            '_f': f,
            '__qualname__': f.__qualname__,
            '__module__': f.__module__,
            '__doc__': f.__doc__
        })
        cls.__instances = {}
        return cls

    def __init__(cls, f):  # only needed in 3.5 and below
        pass

    def __getitem__(cls, item):
        if not isinstance(item, tuple):
            item = (item,)
        try:
            return cls.__instances[item]
        except KeyError:
            cls.__instances[item] = c = cls._f(*item)
            item_repr = '[' + ', '.join(repr(i) for i in item) + ']'
            c.__name__ = cls.__name__ + item_repr
            c.__qualname__ = cls.__qualname__ + item_repr
            c.__template__ = cls
            return c

    def __subclasscheck__(cls, subclass):
        for c in subclass.mro():
            if getattr(c, '__template__', None) == cls:
                return True
        return False

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __repr__(cls):
        import inspect
        return '<template {!r}>'.format('{}.{}[{}]'.format(
            cls.__module__, cls.__qualname__, str(inspect.signature(cls._f))[1:-1]
        ))