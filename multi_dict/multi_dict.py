"""A multi-dimensional dict."""


from collections import defaultdict


class MultiDict(object):
    """A multi-dimensional default dict."""
    
    # TODO: implement get(*args)
    # TODO: implement set(*args)
    # TODO: implement del(*args)
    
    def __init__(self, levels, default):
        """An instance whose number of keys is 'levels' and whose values are created by the
        constructor 'default'.
        """
        self._levels = levels
        if self._levels < 2:
            raise Exception(u'MultiDict can only be constructed for 2 or more dimensions')
        if self._levels == 2:
            self._data = defaultdict(lambda:InnerMultiDict(default))
        else:
            self._data = defaultdict(lambda: MultiDict(self._levels - 1, default))
      
    def __delitem__(self, key):
        del self._data[key]
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __str__(self):
        # What are we doing?
        # Use iteritems() to get all of the items
        # call str() for each entry in the items
        # join all of the strings for the item with ':'
        # join all of the items' strings with ', '
        # surround the whole thing in {}.
        # TODO: could we do this by calling str on the whole thing?
        # return u'{%s}' % u', '.join(u':'.join(map(str, e)) for e in self.iteritems())
        return u'{%s}' % (u', '.join([u'%s:%s' % (str(k), str(v)) for k,v in self._data.iteritems()]))
    
    def __repr__(self):
        return self.__str__()
    
    def iteritems(self):
        """Return items from this object."""   
        for k, v in self._data.iteritems():
            for v_items in v.iteritems():
                yield [k] + v_items
  
  def _put(self, array):
    """Internal version of put() which doesn't check dims to speed insertion of long items."""
        
    if self._dims == 2:
      self._data[array[0]] = array[1]
    else:
      self._data[array[0]]._put(array[1:])


class InnerMultiDict(MultiDict):
    """Implementation of MultiDict for only 2 dimensions."""
    def __init__(self, default):
        self._data = defaultdict(default)
    
    def __str__(self):
        return str(dict(self._data))
    
    def get(self, key):
        return self._data[key]
    
    def iteritems(self):
        for (k, v) in self._data.iteritems():
            yield gen_resp([k, v])
