from .colour_names import colour_schemes
from .Colour import Colour


class Scheme:
	def __init__(self, colours=None, name=None):
		if colours is not None:
			self._colours = [c if isinstance(c, Colour) else Colour.from_hexadecimal(hexadecimal=c) for c in colours]
		else:
			self._colours = [Colour.from_hexadecimal(hexadecimal=c) for c in colour_schemes[name.lower()]]
		self._name = name
		self._rotating_index = 0

	@classmethod
	def auto(cls, obj, copy=False):
		"""
		:type obj: Scheme or list[str] or str
		:rtype: Scheme
		"""
		if isinstance(obj, cls):
			if copy:
				return obj.copy()
			else:
				return obj
		elif isinstance(obj, list):
			return cls(colours=[Colour.auto(obj=x, copy=copy) for x in obj])
		elif isinstance(obj, str):
			return cls(name=obj)
		else:
			raise TypeError('obj should be one of Scheme, list, or str!')

	@property
	def num_colours(self):
		return len(self.colours)

	def pick(self, index=None):
		if index is None:
			index = self._rotating_index
			self._rotating_index = (self._rotating_index + 1) % self.num_colours
		return self.colours[index % self.num_colours]

	def copy(self):
		return self.__class__(colours=[colour.copy() for colour in self.colours], name=self._name)

	@property
	def _max_name_length(self):
		return max([len(colour.name) for colour in self.colours]) + 2

	@property
	def colours(self):
		"""
		:rtype: list[Colour]
		"""
		if any([c is None for c in self._colours]):
			for c in self._colours:
				print(c)
			raise TypeError('colour is None!')
		return self._colours

	def display(self):
		for colour in self.colours:
			colour.display(length=self._max_name_length)

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

	def invert(self):
		"""
		:rtype: Scheme
		"""
		return self.__class__(colours=[~colour for colour in self.colours])

	def __invert__(self):
		return self.invert()

	def darken(self, ratio=0.5):
		return self.__class__(colours=[colour.darken(ratio=ratio) for colour in self.colours])

	def lighten(self, ratio=0.5):
		return self.__class__(colours=[colour.lighten(ratio=ratio) for colour in self.colours])

	brighten = lighten
