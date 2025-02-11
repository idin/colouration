import unittest
from colouration.Gradient import Gradient
from colouration.Colour import Colour

class TestGradient(unittest.TestCase):

    def test_initialization(self):
        gradient = Gradient(colour_1=Colour(red=0.5, green=0.5, blue=0.5), colour_2=Colour(red=0.2, green=0.2, blue=0.2))
        self.assertIsInstance(gradient, Gradient)

    def test_get(self):
        gradient = Gradient(colour_1=Colour(red=0.5, green=0.5, blue=0.5), colour_2=Colour(red=0.2, green=0.2, blue=0.2))
        colour = gradient.get(ratio=0.5)
        self.assertIsInstance(colour, Colour)

if __name__ == '__main__':
    unittest.main() 