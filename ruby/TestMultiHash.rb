$:.unshift File.join(File.dirname(__FILE__))

require "MultiHash"

class TestMultiHash
  def TestOneLevel
    hash = MultiHash.OneLevelHash.new(Integer)
    
    puts hash[0]
    
    hash[1] = "one"
    puts hash[1]
  end
end


hash = OneLevelHash.new(0)

puts hash.get(0)
puts hash.get(1)

hash.put([1,"one"])
puts hash.get(1)

puts hash

hash.each do |k,v|
  puts k.to_s + " " + v
end

hash = MultiHash.new(3,0)
hash.put("one","one-two",12)

hash.each do |k,v|
  puts k.to_s + " " + v
end


puts "done with all tests"
