
import os
import sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)),
    u'..')
)

import unittest

'''So we need one class per set of tests that will work with a particular
instance of a MultiDict.  These are the 'fixtures'.  
'''
# from src.multi_dict import MultiDict
from src import multi_dict

# TODO: test len
# TODO: test set, get, del

# TODO: test MD 2
# TODO: test MD 3

# TODO: test invalid set, keys too short, too long
# TODO: test invalid get, keys too short, too long

class EmptyTest(unittest.TestCase):
    
    def setUp(self):
        self.md = multi_dict.MultiDict(2,int)
    
    def tearDown(self):
        del self.md
        unittest.TestCase.tearDown(self)
    
    def testLen(self):
        assert len(self.md) == 0
    
    def testGetValid(self):
        assert self.md[0,0] == 0
    
    def testGetTooShort(self):
        with self.assertRaises(multi_dict.IncorrectNumberOfKeys):
            self.md[0]

class MultiDictBasicTest(unittest.TestCase):
    
    def setUp(self):
        self.md = multi_dict.MultiDict(2,int)
    
    def tearDown(self):
        del self.md
        unittest.TestCase.tearDown(self)
    
    def testPut(self):
        self.md[3, 4] = 34
        assert self.md[3, 4] == 34
        assert len(self.md) == 1

class MultiDict3Test(unittest.TestCase):
    
    def setUp(self):
        self.md = multi_dict.MultiDict(2,int)
        self.md[1,1] = 11
        self.md[1,2] = 12
        self.md[1,3] = 13
        self.md[2,1] = 21
        self.md[2,2] = 22
        self.md[2,3] = 23
    
    def tearDown(self):
        del self.md
        unittest.TestCase.tearDown(self)
    
    def testGet(self):
        assert self.md[2, 3] == 23
        
    def testLen(self):
        assert len(self.md) == 6
    
    def testDel(self):
        del self.md[2, 3]
        assert len(self.md) == 5
    
    def testDelSubDict(self):
        del self.md[2]
        assert len(self.md) == 3
    
    def testDelLeaf(self):
        del self.md[2,2]
        assert len(self.md) == 5
    
    def testValues(self):
        assert sorted(self.md.values()) == sorted([11, 12, 13, 21, 22, 23]) 
    
    def testKeys(self):
        assert sorted(self.md.keys()) == sorted([[1,1], [1,2], [1,3], [2,1], [2,2], [2,3]])

if __name__ == '__main__':
    unittest.main()
