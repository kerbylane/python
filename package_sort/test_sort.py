import unittest
import sort

class TestSort(unittest.TestCase):

    def check(self, width: int, height: int, length: int, mass: int, expected: str):
        self.assertEqual(sort.sort(width, height, length, mass), expected)

    def test_standard(self):
        self.check(10,10,10,10, sort.STANDARD)

    def test_tall(self):
        self.check(10, 200, 10, 10, sort.SPECIAL)

    def test_bulk(self):
        self.check(10,10,10,10**7, sort.SPECIAL)

    def test_reject(self):
        self.check(200, 10,10, 10**7, sort.REJECTED)

    def test_error(self):
        try:
            self.check(0, 0, 0, 0, sort.STANDARD)
            self.fail("no exception raised")
        except Exception as e:
            pass

if __name__ == "__main__":
    unittest.main()