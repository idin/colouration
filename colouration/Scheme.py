from .colour_names import colour_schemes
from .Colour import Colour


class Scheme:
	def __init__(self, colours=None, name=None):
		if colours is not None:
			self._colours = [c if isinstance(c, Colour) else Colour.from_hexadecimal(hexadecimal=c) for c in colours]
		else:
			self._colours = [Colour.from_hexadecimal(hexadecimal=c) for c in colour_schemes[name.lower()]]
		self._name = name

	@property
	def _max_name_length(self):
		return max([len(colour.name) for colour in self.colours]) + 2

	@property
	def colours(self):
		"""
		:rtype: list[Colour]
		"""
		return self._colours

	def display(self):
		for colour in self.colours:
			colour.display(length=self._max_name_length)

	@property
	def colours(self):
		"""
		:rtype: list[Colour]
		"""
		return self._colours

	def adjust(self, hue=None, saturation=None, lightness=None):
		new_colours = []
		for colour in self.colours:
			colour = colour.copy()
			if hue is not None:
				colour.hue = hue
			if saturation is not None:
				colour.saturation = saturation
			if lightness is not None:
				colour.lightness = lightness
			new_colours.append(colour)
		return self.__class__(colours=new_colours)

	def increase(self, hue=0, saturation=0, lightness=0):
		new_colours = []
		for colour in self.colours:
			colour = colour.copy()
			colour.hue += hue
			colour.saturation += saturation
			colour.lightness += lightness
			new_colours.append(colour)
		return self.__class__(colours=new_colours)
