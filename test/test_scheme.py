import unittest
from colouration.Scheme import Scheme
from colouration.Colour import Colour

class TestScheme(unittest.TestCase):

    def test_initialization(self):
        scheme = Scheme(name='pastel19')
        self.assertIsInstance(scheme, Scheme)

    def test_pick_by_index(self):
        scheme = Scheme(name='pastel19')
        colour = scheme.pick_by_index(0)
        self.assertIsInstance(colour, Colour)

    def test_darken(self):
        scheme = Scheme(name='pastel19')
        darkened_scheme = scheme.darken(ratio=0.1)
        self.assertIsInstance(darkened_scheme, Scheme)

    def test_lighten(self):
        scheme = Scheme(name='pastel19')
        lightened_scheme = scheme.lighten(ratio=0.1)
        self.assertIsInstance(lightened_scheme, Scheme)

    def test_invert(self):
        scheme = Scheme(name='pastel19')
        inverted_scheme = scheme.invert()
        self.assertIsInstance(inverted_scheme, Scheme)

if __name__ == '__main__':
    unittest.main() 