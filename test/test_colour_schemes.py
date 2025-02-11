import unittest
from colouration.colour_schemes import hexadecimal_to_name, name_to_hexadecimal, colour_schemes

class TestColourSchemes(unittest.TestCase):

    def test_hexadecimal_to_name(self):
        self.assertIsInstance(hexadecimal_to_name, dict)

    def test_name_to_hexadecimal(self):
        self.assertIsInstance(name_to_hexadecimal, dict)

    def test_colour_schemes(self):
        self.assertIsInstance(colour_schemes, dict)

if __name__ == '__main__':
    unittest.main() 