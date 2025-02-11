import unittest
from colouration.Colour import Colour

class TestColour(unittest.TestCase):

    def test_initialization_with_rgb(self):
        colour = Colour(red=0.5, green=0.5, blue=0.5)
        self.assertEqual(colour.rgb, (0.5, 0.5, 0.5))

    def test_initialization_with_hexadecimal(self):
        colour = Colour(hexadecimal="#808080")
        self.assertEqual(colour.hexadecimal, "#808080")

    def test_initialization_with_name(self):
        colour = Colour(name="gray")
        self.assertEqual(colour.name, "gray")

    def test_darken(self):
        colour = Colour(red=0.5, green=0.5, blue=0.5)
        darker = colour.darken(ratio=0.1)
        self.assertLess(darker.lightness, colour.lightness)

    def test_lighten(self):
        colour = Colour(red=0.5, green=0.5, blue=0.5)
        lighter = colour.lighten(ratio=0.1)
        self.assertGreater(lighter.lightness, colour.lightness)

    def test_saturate(self):
        colour = Colour(red=0.5, green=0.5, blue=0.5)
        saturated = colour.saturate(ratio=0.1)
        self.assertGreater(saturated.saturation, colour.saturation)

    def test_pale(self):
        colour = Colour(red=0.5, green=0.5, blue=0.5)
        assert colour.saturation == 0 # because this colour is grey
        paler = colour.pale(ratio=0.1)
        assert paler.saturation == 0 # because this colour is also grey

        redder_colour = Colour(red=0.8, green=0.2, blue=0.2)
        paler_red = redder_colour.pale(ratio=0.1)
        self.assertLess(paler_red.saturation, redder_colour.saturation)

    def test_invert(self):
        colour = Colour(red=0.5, green=0.5, blue=0.5)
        inverted = colour.invert()
        self.assertEqual(inverted.rgb, (0.5, 0.5, 0.5))

    def test_mix(self):
        colour1 = Colour(red=0.5, green=0.5, blue=0.5)
        colour2 = Colour(red=0.2, green=0.2, blue=0.2)
        mixed = colour1.mix(colours=[colour2])
        self.assertNotEqual(mixed.rgb, colour1.rgb)
        self.assertNotEqual(mixed.rgb, colour2.rgb)

if __name__ == '__main__':
    unittest.main() 