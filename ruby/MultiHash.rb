class MultiHash
  
  @hash = nil
  @levels = nil
  
  def initialize(levels, default)
    @levels = levels
    if @levels < 1
      raise Exception.new("levels must be higher than 1")
    end
    if @levels == 1
      @hash = Hash.new { OneLevelHash.new(default) }
    else
      @hash = Hash.new { MultiHash.new(@levels-1,default) }
    end
  end
  
  def get(*keys)
    return @hash[keys[0]].get(keys[1..-1])
  end
  
  # TODO: how do we update a value, for instance, increment a count?
  def put(*args)
    @hash[args[0]].put(args[1..-1])
  end
  
  def remove(keys)
    # remove any entries matching the keys
  end
  
  def each
    puts "in MultiHash.each level #{@levels}"
    return @hash.each { |k,v| yield([k,v]) }
  end
  
end

class OneLevelHash
  # Just a wrapper around a regular Hash which implements the methods of MultiHash.
  @hash = nil
  
  def initialize(default)
    @hash = Hash.new {default}
  end
  
  def get(key)
    return @hash[key]
  end
  
  def put(args)
    @hash[args[0]] = args[1]
  end
  
  def remove(key)
    @hash.delete(key)
  end
  
  def each
    puts "in OneLevelHash.each"
    return @hash.each { |k,v| yield([k,v]) }
  end
end 