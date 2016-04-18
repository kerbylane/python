"""Functions to work with "multi-dimensional dicts"."""


from collections import defaultdict


class MultiDict(object):
  """A multi-dimensional default dict."""
  
  def __init__(self, dims, inner):
    if dims < 2:
      raise Exception(u'MultiDict requires more than 2 dimensions')
     
    self._dims = dims
    self._inner = inner
    if self._dims == 2:
      self._data = defaultdict(inner)
    else:
      self._data = defaultdict(lambda: MultiDict(self._dims-1, inner))
      
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
    return u'{%s}' % u', '.join(u':'.join(map(str,e)) for e in self.iteritems())
  
  def __repr__(self):
    return self.__str__()
  
  def iteritems(self, fields=None):
    """Return items from this object.
    
    Each item has length self._dims.  The form of the output is determined by the 'fields' argument.
    
    fields : list
      If 'fields' is supplied the response from this method is a dict whose keys are defined by the 
      fields list. The position of the 'fields' values correspond to the dimension of the object
      to which the key is assigned.
      If fields is not supplied the output for each item is an array. 
    """
    if fields:
      if len(fields) != self._dims:
        raise Exception (
          u'length of fields (%d) does not match number of dimensions (%d)' % 
          (len(fields), self._dims) 
        )
      def gen_resp(vals):
        # creates a dict matching up the fields with the values
        return dict(zip(fields,vals))
    else:
      def gen_resp(vals):
        return vals
    
    if self._dims == 2:
      for (k,v) in self._data.iteritems():
        yield gen_resp([k,v])
    else:
      for k,v in self._data.iteritems():
        for v_items in v.iteritems():
          yield gen_resp([k] + v_items)
  
  def apply_function(self, func):
    """Generator which returns the values from applying func to all responses produced by
    invoking iteritems().
    
    func : function
      must accept a single argument, an array made up of the values appearing in iteritems.
    """
    for e in self.iteritems():
      yield func(e)
  
  def put(self, array):
    """Add an entry whose keys/values are defined by array."""
    if len(array) != self._dims:
      raise Exception (u'length of input (%d) does not match number of dimensions (%d)' % 
          (len(array), self._dims) 
      )
    
    self._put(array)
  
  def _put(self, array):
    """Internal version of put() which doesn't check dims to speed insertion of long items."""
        
    if self._dims == 2:
      self._data[array[0]] = array[1]
    else:
      self._data[array[0]]._put(array[1:])

