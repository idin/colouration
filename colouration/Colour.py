import colorsys
from .colour_names import hexadecimal_to_name, name_to_hexadecimal, colour_schemes
from .colourize import colourize


def normalize(x, minimum, maximum):
	return min(1.0, max(0.0, ((x - minimum) / (maximum - minimum))))


class Colour:
	def __init__(self, red=None, green=None, blue=None, min_value=0.0, max_value=1.0, name=None):
		"""
		:type red: float
		:type green: float
		:type blue: float
		:type min_value: float
		:type max_value: float
		:type name: NoneType or str
		"""
		if red is None and green is None and blue is None:
			if name is None:
				raise ValueError('either red green blue should be provided or a name')
			else:
				hexadecimal = name_to_hexadecimal[name.lower()]
				colour = self.from_hexadecimal(hexadecimal=hexadecimal)
				min_value = 0.0
				max_value = 1.0
				red, green, blue = colour.rgb
		self._red = normalize(x=red, minimum=min_value, maximum=max_value)
		self._green = normalize(x=green, minimum=min_value, maximum=max_value)
		self._blue = normalize(x=blue, minimum=min_value, maximum=max_value)
		self._name = name

	def copy(self):
		return self.__class__(red=self.red, green=self.green, blue=self.blue, name=self._name)

	def __str__(self):
		return f'{self.name}: {self.hexadecimal}'

	def __repr__(self):
		return str(self)

	@staticmethod
	def _get_names():
		"""
		:rtype: dict[str,str]
		"""
		return hexadecimal_to_name

	@staticmethod
	def _get_hexadecimals():
		"""
		:rtype: dict[str,str]
		"""
		return name_to_hexadecimal

	@classmethod
	def get_standard_colours(cls):
		return [cls.from_hexadecimal(hexadecimal=hexadecimal, name=name) for hexadecimal, name in cls._get_names().items()]

	@staticmethod
	def get_schemes():
		return colour_schemes.copy()

	@classmethod
	def from_hsl(cls, hue, saturation, lightness, name=None):
		"""
		:type hue: float
		:type saturation: float
		:type lightness: float
		:type name: str
		:rtype: Colour
		"""
		red, green, blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)
		return cls(red=red, green=green, blue=blue, min_value=0, max_value=1, name=name)

	@classmethod
	def from_hsv(cls, hue, saturation, value, name=None):
		"""
		:type hue: float
		:type saturation: float
		:type value: float
		:rtype: Colour
		"""
		red, green, blue = colorsys.hsv_to_rgb(h=hue, s=saturation, v=value)
		return cls(red=red, green=green, blue=blue, min_value=0, max_value=1, name=name)

	@classmethod
	def from_hexadecimal(cls, hexadecimal, name=None):
		"""
		:type hexadecimal: str
		:type name: NoneType or str
		:rtype: Colour
		"""
		if hexadecimal.startswith('#'):
			hexadecimal = hexadecimal[1:]

		if len(hexadecimal) == 3:
			hexadecimal = \
				hexadecimal[0] + hexadecimal[0] + \
				hexadecimal[1] + hexadecimal[1] + \
				hexadecimal[2] + hexadecimal[2]

		if len(hexadecimal) != 6:
			raise ValueError('The hex value should be 3 or 6 characters long!')

		red = int(f"0x{hexadecimal[0:2]}", 16)
		green = int(f"0x{hexadecimal[2:4]}", 16)
		blue = int(f"0x{hexadecimal[4:6]}", 16)

		return cls(red=red, green=green, blue=blue, min_value=0.0, max_value=255, name=name)

	@property
	def red(self):
		return self._red

	@property
	def green(self):
		return self._green

	@property
	def blue(self):
		return self._blue

	@property
	def name(self):
		if self._name is not None:
			return self._name
		else:
			return self.find_nearest(colours=self.get_standard_colours()).name

	@property
	def rgb(self):
		return self.red, self.green, self.blue

	@property
	def hsl(self):
		h, l, s = colorsys.rgb_to_hls(r=self.red, g=self.green, b=self.blue)
		return h, s, l

	@property
	def yig(self):
		return colorsys.rgb_to_yiq(r=self.red, g=self.green, b=self.blue)

	@property
	def hsv(self):
		return colorsys.rgb_to_hsv(r=self.red, g=self.green, b=self.blue)

	@property
	def hue(self):
		return self.hsl[0]

	@hue.setter
	def hue(self, hue):
		_, saturation, lightness = self.hsl
		self._red, self._green, self._blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)

	@property
	def saturation(self):
		return self.hsl[1]

	@saturation.setter
	def saturation(self, saturation):
		hue, _, lightness = self.hsl
		self._red, self._green, self._blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)

	@property
	def lightness(self):
		return self.hsl[2]

	@lightness.setter
	def lightness(self, lightness):
		hue, saturation, _ = self.hsl
		self._red, self._green, self._blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)

	@property
	def value(self):
		return self.hsv[2]

	@property
	def hexadecimal(self):
		r = int(min(max(0.0, self.red * 255), 255))
		g = int(min(max(0.0, self.green * 255), 255))
		b = int(min(max(0.0, self.blue * 255), 255))
		return '#{:02x}{:02x}{:02x}'.format(r, g, b)

	def get_distance(self, other):
		"""
		:type other: Colour
		:rtype: float
		"""
		red2 = (self.red - other.red) ** 2
		green2 = (self.green - other.green) ** 2
		blue2 = (self.blue - other.blue) ** 2
		return (red2 + green2 + blue2) ** 0.5

	def find_nearest(self, colours):
		"""
		:type colours: list[Colour]
		:rtype:
		"""
		return sorted(colours, key=lambda x: self.get_distance(other=x))[0]

	def __add__(self, other):
		"""
		:type other: Colour
		:rtype: Colour
		"""
		red = (self.red + other.red) / 2.0
		green = (self.green + other.green) / 2.0
		blue = (self.blue + other.blue) / 2.0
		return self.__class__(red=red, green=green, blue=blue)

	def __getstate__(self):
		return self.red, self.green, self.blue, self._name

	def __setstate__(self, state):
		self._red, self._green, self._blue, self._name = state

	def colourize(self, string, background='auto'):
		if background == 'auto':
			background = self.__class__(name='white') if self.lightness < 0.5 else self.__class__(name='black')

		if background is not None:
			bg_red, bg_green, bg_blue = background.rgb
		else:
			bg_red, bg_green, bg_blue = None, None, None

		return colourize(
			string=string, red=self.red, green=self.green, blue=self.blue,
			bg_red=bg_red, bg_green=bg_green, bg_blue=bg_blue
		)

	def colourize_background(self, string, text_colour='auto'):
		if text_colour == 'auto':
			text_colour = self.__class__(name='white') if self.lightness < 0.5 else self.__class__(name='black')

		if text_colour is not None:
			bg_red, bg_green, bg_blue = text_colour.rgb
		else:
			bg_red, bg_green, bg_blue = self.__class__.from_hexadecimal(hexadecimal='#808080').rgb

		return colourize(
			string=string, bg_red=self.red, bg_green=self.green, bg_blue=self.blue,
			red=bg_red, green=bg_green, blue=bg_blue
		)

	def print(self, string, secondary='auto', end=None, main_colour='background'):
		if main_colour == 'background':
			print(self.colourize_background(string=string, text_colour=secondary), end=end)
		else:
			print(self.colourize(string=string, background=secondary), end=end)

	def display(self, string=None, secondary='auto', end=None, main_colour='background', length=None):
		string = string or f' {self.name} '
		if length is not None:
			string = ('{:^' + str(int(length)) + '}').format(string)
		self.print(string=string, secondary=secondary, end=end, main_colour=main_colour)
