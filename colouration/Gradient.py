from .Colour import Colour


class Gradient:
	def __init__(self, colour_1, colour_2, num_levels=10):
		"""
		Initializes a Gradient object.

		Args:
			colour_1: The first Colour object.
			colour_2: The second Colour object.
			num_levels: The number of levels in the gradient.
		"""
		colour_1 = Colour(colour_1)
		colour_2 = Colour(colour_2)

		self._colours = [
			(colour_1 * (num_levels - i - 1)).mix(colour_2 * i)
			for i in range(num_levels)
		]
		self._num_levels = num_levels

	def __repr__(self):
		"""Returns a string representation of the gradient."""
		return '\n'.join([repr(colour) for colour in self._colours])

	def colourize(self, string: str) -> str:
		"""
		Colourizes a string with the gradient.

		Args:
			string: The string to colourize.

		Returns:
			str: The colourized string.
		"""
		denominator = len(string) - 1
		return ''.join([
			self.get(ratio=numerator / denominator).colourize(string=character, background=None)
			for numerator, character in enumerate(string)
		])

	def get(self, ratio: float) -> Colour:
		"""
		Gets the colour at a specific ratio in the gradient.

		Args:
			ratio: The ratio (0.0-1.0).

		Returns:
			Colour: The Colour object at the specified ratio.
		"""
		ratio = max(0.0, min(1.0, ratio))
		return self._colours[round(ratio * (self._num_levels - 1))]
