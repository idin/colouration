import unittest
from colouration.convert_rgb_to_hsl import convert_rgb_to_hsl

class TestConvertRGBToHSL(unittest.TestCase):

    def test_conversion(self):
        hsl = convert_rgb_to_hsl(red=0.5, green=0.5, blue=0.5)
        self.assertIsInstance(hsl, tuple)
        self.assertEqual(len(hsl), 3)

if __name__ == '__main__':
    unittest.main() 