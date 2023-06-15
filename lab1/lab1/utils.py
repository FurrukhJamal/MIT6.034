# from UserDict import DictMixin
class DictMixin:
    def __init__(self, *args, **kwargs):
        self.data = {}
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        return key in self.data

    def keys(self):
        return list(self.data.keys())

    def items(self):
        return list(self.data.items())

    def values(self):
        return list(self.data.values())

    def get(self, key, default=None):
        return self.data.get(key, default)

    def update(self, *args, **kwargs):
        if len(args) > 1:
            raise TypeError("update expected at most 1 argument, got {}".format(len(args)))
        elif args:
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def clear(self):
        self.data.clear()

    def copy(self):
        return DictMixin(self.data)

    def setdefault(self, key, default=None):
        if key not in self.data:
            self.data[key] = default
        return self.data[key]

    def pop(self, key, default=None):
        if key in self.data:
            value = self.data[key]
            del self.data[key]
            return value
        else:
            return default

    def popitem(self):
        if self.data:
            key = next(iter(self.data))
            value = self.data.pop(key)
            return (key, value)
        else:
            raise KeyError("popitem(): dictionary is empty")





import re

class ClobberedDictKey(Exception):
    "A flag that a variable has been assigned two incompatible values."
    pass

class NoClobberDict(DictMixin):
    """
    A dictionary-like object that prevents its values from being
    overwritten by different values. If that happens, it indicates a
    failure to match.
    """
    def __init__(self, initial_dict = None):
        if initial_dict == None:
            self._dict = {}
        else:
            self._dict = dict(initial_dict)
        
    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        # if self._dict.has_key(key) and self._dict[key] != value:
        if key in self._dict and self._dict[key] != value:
            raise ClobberedDictKey(key, value)

        self._dict[key] = value

    def __delitem__(self, key):
        del self._dict[key]

    def __contains__(self, key):
        return self._dict.__contains__(key)

    def __iter__(self):
        return self._dict.__iter__()

    def iteritems(self):
        return self._dict.iteritems()
        
    def keys(self):
        return self._dict.keys()

# A regular expression for finding variables.
AIRegex = re.compile(r'\(\?(\S+)\)')

# def AIStringToRegex(AIStr):
#     return AIRegex.sub( r'(?P<\1>\S+)', AIStr )+'$'

def AIStringToRegex(AIStr):
    return AIRegex.sub(lambda m: '(?P<{}>\S+)'.format(m.group(1)), AIStr) + '$'


def AIStringToPyTemplate(AIStr):
    return AIRegex.sub( r'%(\1)s', AIStr )

def AIStringVars(AIStr):
    # This is not the fastest way of doing things, but
    # it is probably the most explicit and robust
    return set([ AIRegex.sub(r'\1', x) for x in AIRegex.findall(AIStr) ])

