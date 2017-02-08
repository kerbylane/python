"""A multi-dimensional dict."""

from collections import defaultdict

class IncorrectNumberOfKeys(Exception):
    pass

class MultiDict(object):
    """A multi-dimensional default dict.
    
    This provides functions to simplify interactions with a nested defaultdict structure.
    It is assumed that 'values' are only at the lowest level of the structure.  Hence get()
    requires an array as long as the 'levels' argument used in the constructor.
    """
    
    # The methods that make it possible to use the [] notation, such as __setitem__,
    # include tests for key length.  But they call internal methods that no longer
    # test the arguments for faster performance.
    
    def __init__(self, levels, default):
        """An instance whose number of keys is 'levels' and whose values are created by the
        constructor 'default'.
        """
        if levels < 2:
            raise Exception(u'MultiDict can only be constructed for 2 or more dimensions')
        
        self._levels = levels
        if self._levels == 2:
            self._data = defaultdict(lambda: InnerMultiDict(default))
        else:
            self._data = defaultdict(lambda: MultiDict(self._levels - 1, default))
    
    def __setitem__(self, *args):
        # print 'md.__setitems__ args is %s' % str(args)
        # keys = self._getKeys(args[0])
        self._checkLength(args[0])
        self._set(args[0], args[1])
    
    def __getitem__(self, *keys):
        # print 'md.__getitem__ keys is %s' % str(keys)
        self._checkLength(keys[0])
        return self._get(keys[0])
      
    def __delitem__(self, keys):
        if isinstance(keys, tuple):
            del self._data[keys[0]][ keys[1:] ]
            # If the sub-dict is empty dump it
            if len(self._data[keys[0]]) == 0:
                self._data.__delitem__(keys[0])
        else:
            del self._data[keys]
    
    def __str__(self):
        # This is really complicated.  What are we doing?
        # Use iteritems() to get all of the items
        # call str() for each entry in the items
        # join all of the strings for the item with ':'
        # join all of the items' strings with ', '
        # surround the whole thing in {}.
        
        return u'{%s}' % u', '.join([u'%s:%s' % (str(k), str(v)) for k,v in self._data.iteritems()])
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        """Returns a count of all 'leaves' in the structure."""
        return sum(v.__len__() for v in self._data.values())
    
    def iteritems(self):
        """Return items from this object."""
        for k, v in self._data.iteritems():
            for v_items in v.iteritems():
                yield [k] + v_items
                
    def get(self, *keys):
        """Returns subdict sharing keys prefix."""
        if len(keys) > self._levels:
            raise IncorrectNumberOfKeys("Too many keys submitted, got %d, max is %d" % (len(keys), self._levels))
        
        return self._get(keys)
    
    def keys(self):
        for entry in self.iteritems():
            yield entry[:-1]
    
    def values(self):
        for entry in self.iteritems():
            yield entry[-1]
    
    ##################################################
    #
    # The following are internal only functions.  Some are intended to avoid tests that
    # only need to be performed at the top API level.
    #
    ##################################################
    
    def _checkLength(self, args):
        """Confirm the number of keys submitted matches the number of _levels."""
        if not (isinstance(args, tuple) and len(args) == self._levels):
            raise IncorrectNumberOfKeys('Got key argument %d, length should be %d' % (args, self._levels))
  
    def _set(self, keys, value):
        """Internal version of set() which doesn't check dims to speed insertion of long items."""
        print 'md._set (%d) %s %s' % (self._levels, str(keys), str(value))
        self._data.__getitem__(keys[0])._set(keys[1:], value)
    
    def _get(self, keys):
        print 'md._get %s' % str(keys)
        if len(keys) == 1:
            return self._data.__getitem__(keys[0])
        else:
            return self._data.__getitem__(keys[0])._get(keys[1:])


class InnerMultiDict(MultiDict):
    """Implementation of MultiDict for only 2 dimensions.
    
    This is just a wrapper around defaultdict which supports the same API as MultiDict."""
    
    # Note that the key arguments passed are all arrays with 1 entry.  This makes the
    # code in MultiDict cleaner.
    
    def __init__(self, default):
        self._data = defaultdict(default)
    
    def __setitem__(self, *args):
        # print 'id.__setitem__ args: %s' % str(args)
        self._data.__setitem__(args[0][0], args[1])
    
    def __getitem__(self, key):
        # print 'id.__getitem__ key is %s' % str(key)
        return self._data.__getitem__(key[0])
      
    def __delitem__(self, key):
        self._data.__delitem__(key[0])
    
    def __str__(self):
        return str(dict(self._data))
        
    def __len__(self):
        return self._data.__len__()
    
    def _set(self, key, value):
        print 'id._set %s %s' % (str(key[0]), str(value))
        self._data.__setitem__(key[0], value)
    
    def _get(self, key):
        print 'id._get %s' % str(key[0])
        return self._data[key[0]]
    
    def iteritems(self):
        for (k, v) in self._data.iteritems():
            yield [k, v]
