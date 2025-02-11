import unittest
from colouration.colourize import colourize

class TestColourize(unittest.TestCase):

    def test_colourize(self):
        result = colourize(string="Hello", red=0.5, green=0.5, blue=0.5)
        self.assertIsInstance(result, str)

if __name__ == '__main__':
    unittest.main() 