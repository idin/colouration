import colorsys
from .colour_schemes import hexadecimal_to_name, name_to_hexadecimal, colour_schemes
from .colourize import colourize
from typing import Union, Optional

DEFAULT_INCREASE_RATIO = 0.2
DEFAULT_INCREASE_AMOUNT = 0.1


def scale(x: float, minimum: float, maximum: float) -> float:
	"""Scales a value between a minimum and maximum range."""
	return (x - minimum) / (maximum - minimum)


def limit(x: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
	"""Limits a value to be within a specified range."""
	return min(maximum, max(minimum, x))


class Colour:
	def __init__(
			self, 
			obj: Optional[Union[str, 'Colour', tuple, list]] = None, 
			red: Optional[float] = None, 
			green: Optional[float] = None, 
			blue: Optional[float] = None, 
			hexadecimal: Optional[str] = None,
			hue: Optional[float] = None, 
			saturation: Optional[float] = None, 
			lightness: Optional[float] = None, 
			value: Optional[float] = None,
			min_value: float = 0.0, 
			max_value: float = 1.0, 
			name: Optional[str] = None, 
			id: Optional[int] = None, 
			scheme: Optional[any] = None,
			weight: float = 1.0
	):
		"""
		Initializes a Colour object.

		Args:
			obj: A string, Colour object, or a tuple/list of RGB values.
			red: Red component of the colour.
			green: Green component of the colour.
			blue: Blue component of the colour.
			hexadecimal: Hexadecimal string representation of the colour.
			hue: Hue component for HSL/HSV.
			saturation: Saturation component for HSL/HSV.
			lightness: Lightness component for HSL.
			value: Value component for HSV.
			min_value: Minimum value for scaling.
			max_value: Maximum value for scaling.
			name: Name of the colour.
			id: Identifier for the colour.
			scheme: Colour scheme associated with the colour.
			weight: Weight of the colour.
		"""
		self._id = id
		self._scheme = scheme
		self._weight = weight
		assert isinstance(obj, (str, self.__class__, tuple, list)) or obj is None, f'obj should be one of str, Colour, tuple, or list but it is {type(obj)}'

		if obj is not None:
			if isinstance(obj, self.__class__):
				red, green, blue = obj.rgb

			elif isinstance(obj, str):
				if obj.startswith('#'):
					hexadecimal = obj

				else:
					name = obj

			elif isinstance(obj, (list, tuple)):
				if len(obj) == 3:
					red, green, blue = obj
				else:
					raise ValueError(f'obj should be a tuple/list of 3 values but it is {obj}')

			else:
				raise TypeError(f'obj should be one of str, Colour, tuple, or list but it is {type(obj)}')
			min_value = 0.0
			max_value = 1.0

		if red is not None and green is not None and blue is not None:
			pass

		elif hue is not None and saturation is not None and lightness is not None:
			red, green, blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)
			min_value = 0.0
			max_value = 1.0

		elif hue is not None and saturation is not None and value is not None:
			red, green, blue = colorsys.hsv_to_rgb(h=hue, s=saturation, v=value)
			min_value = 0.0
			max_value = 1.0

		elif hexadecimal is not None:
			red, green, blue = self.convert_hexadecimal_to_rgb(hexadecimal=hexadecimal)
			min_value = 0.0
			max_value = 255.0

		elif name is not None:
			if name.lower() not in name_to_hexadecimal:
				raise ValueError(f'name: "{name}" not acceptable. It is of type "{type(name)}". Other names are: {list(name_to_hexadecimal.keys())}')
			hexadecimal = name_to_hexadecimal[name.lower()]
			red, green, blue = self.convert_hexadecimal_to_rgb(hexadecimal=hexadecimal)
			min_value = 0.0
			max_value = 255.0

		else:
			raise ValueError(f'obj: "{obj}" not acceptable. It is of type "{type(obj)}"')

		self._red = scale(x=red, minimum=min_value, maximum=max_value)
		self._green = scale(x=green, minimum=min_value, maximum=max_value)
		self._blue = scale(x=blue, minimum=min_value, maximum=max_value)
		self._name = name

	@property
	def scheme(self) -> any:
		"""
		Returns the colour scheme associated with the colour.

		Returns:
			Scheme or NoneType: The colour scheme.
		"""
		return self._scheme

	@property
	def id(self) -> int | None:
		"""
		Returns the identifier of the colour.

		Returns:
			int or NoneType: The identifier.
		"""
		return self._id

	def use(self, log=None):
		"""
		Logs the usage of a colour.

		Args:
			log: Optional log information.
		"""
		if self.scheme is not None:
			self.scheme.use(colour=self, log=log)

	@property
	def logs(self) -> list[dict] | None:
		"""Returns the usage logs of the colour."""
		if self.scheme is not None:
			return self.scheme._usage_logs[self.id]
		else:
			return None

	@property
	def usage(self) -> int:
		"""
		Returns the usage count of the colour.

		Returns:
			int: The usage count.
		"""
		if self.scheme is not None:
			return self.scheme.get_usage(colour=self)
		else:
			return 0

	def __delete_identity(self):
		"""Deletes the identity attributes of the colour."""
		self._name = None
		self._id = None
		self._scheme = None

	@property
	def red(self) -> float:
		"""Returns the red component of the colour."""
		return limit(x=self._red)

	@red.setter
	def red(self, red: float):
		"""Sets the red component of the colour."""
		self.__delete_identity()
		self._red = red

	@property
	def green(self) -> float:
		"""Returns the green component of the colour."""
		return limit(x=self._green)

	@green.setter
	def green(self, green: float):
		"""Sets the green component of the colour."""
		self.__delete_identity()
		self._green = green

	@property
	def blue(self) -> float:
		"""Returns the blue component of the colour."""
		return limit(x=self._blue)

	@blue.setter
	def blue(self, blue: float):
		"""Sets the blue component of the colour."""
		self.__delete_identity()
		self._blue = blue

	def copy(self, keep_id=True):
		"""
		Creates a copy of the colour.

		Args:
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: A copy of the colour.
		"""
		if keep_id:
			return self.__class__(
				red=self.red, green=self.green, blue=self.blue, name=self._name, id=self._id, scheme=self._scheme,
				weight=self._weight
			)
		else:
			return self.__class__(
				red=self.red, green=self.green, blue=self.blue, name=self._name, id=None, scheme=None,
				weight=self._weight
			)

	def __str__(self) -> str:
		"""Returns a string representation of the colour."""
		return f'{self.name}: {self.hexadecimal}'

	def __repr__(self) -> str:
		"""Returns a string representation of the colour."""
		return str(self)

	@staticmethod
	def _get_names() -> dict[str, str]:
		"""
		Returns a dictionary mapping hexadecimals to names.

		Returns:
			dict[str, str]: The mapping of hexadecimals to names.
		"""
		return hexadecimal_to_name

	@staticmethod
	def _get_hexadecimals() -> dict[str, str]:
		"""
		Returns a dictionary mapping names to hexadecimals.

		Returns:
			dict[str, str]: The mapping of names to hexadecimals.
		"""
		return name_to_hexadecimal

	@classmethod
	def get_standard_colours(cls) -> list['Colour']:
		"""
		Returns a list of standard colours.

		Returns:
			list[Colour]: The list of standard colours.
		"""
		return [cls(hexadecimal=hexadecimal, name=name) for hexadecimal, name in cls._get_names().items()]

	@staticmethod
	def get_schemes() -> dict[str, list[str]]:
		"""
		Returns a copy of the colour schemes.

		Returns:
			dict[str, list[str]]: The colour schemes.
		"""
		return colour_schemes.copy()

	@staticmethod
	def convert_hexadecimal_to_rgb(hexadecimal: str) -> tuple[int, int, int]:
		"""
		Converts a hexadecimal string to RGB values.

		Args:
			hexadecimal: The hexadecimal string.

		Returns:
			tuple: The RGB values.
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
		return red, green, blue

	@property
	def name(self) -> str:
		"""Returns the name of the colour."""
		if self._name is None:
			self._name = self.find_nearest(colours=self.get_standard_colours()).name
		return self._name

	@property
	def rgb(self) -> tuple[int, int, int]:
		"""
		Returns the RGB values of the colour.

		Returns:
			tuple: The RGB values.
		"""
		return self.red, self.green, self.blue

	@property
	def hsl(self) -> tuple[float, float, float]:
		"""
		Returns the HSL values of the colour.

		Returns:
			tuple: The HSL values.
		"""
		h, l, s = colorsys.rgb_to_hls(r=self.red, g=self.green, b=self.blue)
		return h, s, l

	@property
	def yiq(self) -> tuple[float, float, float]:
		"""
		Returns the YIQ values of the colour.

		Returns:
			tuple: The YIQ values.
		"""
		return colorsys.rgb_to_yiq(r=self.red, g=self.green, b=self.blue)

	@property
	def hsv(self) -> tuple[float, float, float]:
		"""
		Returns the HSV values of the colour.

		Returns:
			tuple: The HSV values.
		"""
		return colorsys.rgb_to_hsv(r=self.red, g=self.green, b=self.blue)

	@property
	def hue(self) -> float:
		"""
		Returns the hue of the colour.

		Returns:
			float: The hue.
		"""
		return self.hsl[0]

	@hue.setter
	def hue(self, hue: float):
		"""Sets the hue of the colour."""
		_, saturation, lightness = self.hsl
		hue = hue % 1.0
		self.__delete_identity()
		self.red, self._green, self._blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)

	@property
	def saturation(self) -> float:
		"""
		Returns the saturation of the colour.

		Returns:
			float: The saturation.
		"""
		return self.hsl[1]

	@saturation.setter
	def saturation(self, saturation: float):
		"""Sets the saturation of the colour."""
		saturation = min(1.0, max(0, saturation))
		hue, _, lightness = self.hsl
		self._name = None
		self.red, self._green, self._blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)

	def set_lightness_and_saturation(self, lightness: float, saturation: float):
		"""Sets the lightness and saturation of the colour."""
		hue = self.hue
		self.red, self._green, self._blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)

	@property
	def lightness(self) -> float:
		"""
		Returns the lightness of the colour.

		Returns:
			float: The lightness.
		"""
		return self.hsl[2]

	@lightness.setter
	def lightness(self, lightness: float):
		"""Sets the lightness of the colour."""
		lightness = min(1.0, max(0.0, lightness))
		hue, saturation, _ = self.hsl
		self._name = None
		self.red, self._green, self._blue = colorsys.hls_to_rgb(h=hue, l=lightness, s=saturation)

	@property
	def value(self) -> float:
		"""
		Returns the value of the colour.

		Returns:
			float: The value.
		"""
		return self.hsv[2]

	@value.setter
	def value(self, value: float):
		"""Sets the value of the colour."""
		value = min(1.0, max(0.0, value))
		hue, saturation, _ = self.hsv
		self._name = None
		self.red, self._green, self._blue = colorsys.hsv_to_rgb(h=hue, v=value, s=saturation)

	@property
	def hexadecimal(self) -> str:
		"""
		Returns the hexadecimal representation of the colour.

		Returns:
			str: The hexadecimal string.
		"""
		r = int(min(max(0.0, self.red * 255), 255))
		g = int(min(max(0.0, self.green * 255), 255))
		b = int(min(max(0.0, self.blue * 255), 255))
		return '#{:02x}{:02x}{:02x}'.format(r, g, b)

	def get_hexadecimal(self, opacity: float | None = None) -> str:
		"""
		Returns the hexadecimal representation of the colour with optional opacity.

		Args:
			opacity: Opacity value.

		Returns:
			str: The hexadecimal string.
		"""
		if opacity is None:
			result = self.hexadecimal
		else:
			o = int(min(max(0.0, opacity * 255), 255))
			result = '{}{:02x}'.format(self.hexadecimal, o)
		return result

	def get_distance(self, other: 'Colour') -> float:
		"""
		Calculates the distance between this colour and another.

		Args:
			other: The other Colour object.

		Returns:
			float: The distance.
		"""
		red2 = (self.red - other.red) ** 2
		green2 = (self.green - other.green) ** 2
		blue2 = (self.blue - other.blue) ** 2
		return (red2 + green2 + blue2) ** 0.5

	def find_nearest(self, colours: list['Colour']) -> 'Colour':
		"""
		Finds the nearest colour from a list of colours.

		Args:
			colours: List of Colour objects.

		Returns:
			Colour: The nearest colour.
		"""
		return sorted(colours, key=lambda x: self.get_distance(other=x))[0]

	def limit(self):
		"""Limits the RGB components to be within the valid range."""
		self._red = self.red
		self._green = self.green
		self._blue = self.blue

	@classmethod
	def _tuple_as_colour(cls, other: tuple | list) -> 'Colour':
		"""Converts a tuple or list to a Colour object."""
		if isinstance(other, (tuple, list)):
			if len(other) == 3:
				other = cls(red=other[0], green=other[1], blue=other[2])
		return other

	def __add__(self, other: Union['Colour', tuple, list]) -> 'Colour':
		"""
		Adds another colour or value to this colour.

		Args:
			other: The other Colour object or a numeric value.

		Returns:
			Colour: The resulting Colour object.
		"""
		other = self._tuple_as_colour(other=other)

		if isinstance(other, Colour):
			return self.__class__(
				red=self._red + other._red,
				green=self._green + other._green,
				blue=self._blue + other._blue,
				weight=self._weight
			)
		else:
			return self.__class__(
				red=self._red + other, green=self._green + other, blue=self._blue + other, weight=self._weight
			)

	def __sub__(self, other: Union['Colour', tuple, list]) -> 'Colour':
		"""
		Subtracts another colour from this colour.

		Args:
			other: The other Colour object.

		Returns:
			Colour: The resulting Colour object.
		"""
		other = self._tuple_as_colour(other=other)

		return self.__class__(
			red=self._red - other._red,
			green=self._green - other._green,
			blue=self._blue - other._blue
		)

	def __mul__(self, other: Union['Colour', tuple, list]) -> 'Colour':
		"""
		Multiplies this colour by another colour or value.

		Args:
			other: The other Colour object or a numeric value.

		Returns:
			Colour: The resulting Colour object.
		"""
		if isinstance(other, (list, tuple)):
			other = self._tuple_as_colour(other=other)

		if isinstance(other, Colour):
			return self.__class__(
				red=self.red * other.red,
				green=self.green * other.green,
				blue=self.blue * other.blue
			)
		else:
			return self.__class__(red=self._red, green=self._green, blue=self._blue, weight=self._weight * other)

	def __neg__(self) -> 'Colour':
		"""
		Negates the colour.

		Returns:
			Colour: The negated Colour object.
		"""
		return self.__class__(red=1 - self.red, green=1 - self.green, blue=1 - self.blue)

	def __invert__(self) -> 'Colour':
		"""Inverts the colour."""
		return -self

	def __and__(self, other: Union['Colour', tuple, list]) -> 'Colour':
		"""
		Performs a bitwise AND operation with another colour or value.

		Args:
			other: The other Colour object or a numeric value.

		Returns:
			Colour: The resulting Colour object.
		"""
		if isinstance(other, (int, float)):
			if other > 1 or other < 0:
				raise ValueError('other cannot be negative or greater than one.')
		other = self._tuple_as_colour(other=other)

		return self * other

	def __or__(self, other: Union['Colour', tuple, list]) -> 'Colour':
		"""
		Performs a bitwise OR operation with another colour or value.

		Args:
			other: The other Colour object or a numeric value.

		Returns:
			Colour: The resulting Colour object.
		"""
		if isinstance(other, (int, float)):
			if other > 1 or other < 0:
				raise ValueError('other cannot be negative or greater than one.')
		other = self._tuple_as_colour(other=other)

		return self + other

	def __hashkey__(self) -> tuple:
		"""Returns a hash key for the colour."""
		return self.__class__.__name__, self.__getstate__()

	def __getstate__(self) -> tuple:
		"""Returns the state of the colour for pickling."""
		return self.red, self.green, self.blue, self._name, self._id, self._weight, None

	def __setstate__(self, state: tuple):
		"""Sets the state of the colour from pickling."""
		self._red, self._green, self._blue, self._name, self._id, self._weight, self._scheme = state

	@classmethod
	def _from_state(cls, state: tuple) -> 'Colour':
		"""Creates a Colour object from a state."""
		red, green, blue, name, id, weight, _ = state
		return cls(red=red, green=green, blue=blue, id=id, weight=weight)

	def colourize(self, string: str, background: str | None = None) -> str:
		"""
		Colourizes a string with the colour.

		Args:
			string: The string to colourize.
			background: The background colour.

		Returns:
			str: The colourized string.
		"""
		if background == 'auto':
			background = self.farthest_gray

		if background is None:
			bg_red, bg_green, bg_blue = None, None, None
		else:
			if not isinstance(background, self.__class__):
				background = self.__class__(obj=background)
			bg_red, bg_green, bg_blue = background.rgb

		return colourize(
			string=string, red=self.red, green=self.green, blue=self.blue,
			bg_red=bg_red, bg_green=bg_green, bg_blue=bg_blue
		)

	def colourize_background(self, string: str, text_colour: str = 'auto') -> str:
		"""
		Colourizes the background of a string.

		Args:
			string: The string to colourize.
			text_colour: The text colour.

		Returns:
			str: The colourized string.
		"""
		if isinstance(text_colour, str) and text_colour == 'auto':
			text_colour = self.farthest_gray

		if text_colour is not None:
			bg_red, bg_green, bg_blue = text_colour.rgb
		else:
			bg_red, bg_green, bg_blue = self.__class__(hexadecimal='#808080').rgb

		return colourize(
			string=string, bg_red=self.red, bg_green=self.green, bg_blue=self.blue,
			red=bg_red, green=bg_green, blue=bg_blue
		)

	def print(self, string: str, secondary: str = 'auto', end: str | None = None, main_colour: str = 'background'):
		"""
		Prints a string with the colour.

		Args:
			string: The string to print.
			secondary: The secondary colour.
			end: The end character.
			main_colour: The main colour.
		"""
		if main_colour == 'background':
			print(self.colourize_background(string=string, text_colour=secondary), end=end)
		else:
			print(self.colourize(string=string, background=secondary), end=end)

	def display(self, string: str | None = None, secondary: str = 'auto', end: str | None = None, main_colour: str = 'background', length: int | None = None):
		"""
		Displays a string with the colour.

		Args:
			string: The string to display.
			secondary: The secondary colour.
			end: The end character.
			main_colour: The main colour.
			length: The length of the string.
		"""
		string = string or f' {self.name} '
		if length is not None:
			string = ('{:^' + str(int(length)) + '}').format(string)
		self.print(string=string, secondary=secondary, end=end, main_colour=main_colour)

	def mix_with_gray(self, gray_weight: float | None = None) -> 'Colour':
		"""
		Mixes the colour with gray.

		Args:
			gray_weight: The weight of the gray.

		Returns:
			Colour: The resulting Colour object.
		"""
		gray = self.nearest_gray
		if gray_weight:
			gray._weight = gray_weight
		return self.mix(colours=gray)

	def darken(self, ratio: float = DEFAULT_INCREASE_RATIO, amount: float | None = None, keep_id: bool = True) -> 'Colour':
		"""
		Darkens the colour.

		Args:
			ratio: The ratio to darken.
			amount: The amount to darken.
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The resulting Colour object.
		"""
		ratio = min(1.0, max(-1.0, ratio))
		darker = self.copy(keep_id=keep_id)

		if amount is None:
			amount = self.lightness ** 0.5 * ratio

		darker.lightness = darker.lightness - amount
		return darker

	def lighten(self, ratio: float = DEFAULT_INCREASE_RATIO, amount: float | None = None, keep_id: bool = True) -> 'Colour':
		"""
		Lightens the colour.

		Args:
			ratio: The ratio to lighten.
			amount: The amount to lighten.
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The resulting Colour object.
		"""
		ratio = min(1.0, max(-1.0, ratio))
		lighter = self.copy(keep_id=keep_id)

		if amount is None:
			amount = (1 - self.lightness) * ratio

		lighter.lightness = lighter.lightness + amount
		return lighter

	def saturate(self, ratio: float = DEFAULT_INCREASE_RATIO, amount: float | None = None, keep_id: bool = True) -> 'Colour':
		"""
		Saturates the colour.

		Args:
			ratio: The ratio to saturate.
			amount: The amount to saturate.
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The resulting Colour object.
		"""
		ratio = min(1.0, max(-1.0, ratio))
		more_saturated = self.copy(keep_id=keep_id)

		if amount is None:
			amount = (1 - self.saturation) * ratio

		more_saturated.saturation = more_saturated.saturation + amount
		return more_saturated

	def pale(self, ratio: float = DEFAULT_INCREASE_RATIO, amount: float | None = None, keep_id: bool = True) -> 'Colour':
		"""
		Desaturates the colour.

		Args:
			ratio: The ratio to desaturate.
			amount: The amount to desaturate.
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The resulting Colour object.
		"""
		ratio = min(1.0, max(-1.0, ratio))
		less_saturated = self.copy(keep_id=keep_id)

		if amount is None:
			amount = self.saturation * ratio

		less_saturated.saturation = less_saturated.saturation - amount
		return less_saturated

	def darken_or_lighten(self, ratio: float = DEFAULT_INCREASE_RATIO, amount: float | None = None, keep_id: bool = True) -> 'Colour':
		"""
		Darkens or lightens the colour based on its lightness.

		Args:
			ratio: The ratio to adjust.
			amount: The amount to adjust.
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The resulting Colour object.
		"""
		if self.lightness <= 0.5:
			return self.lighten(ratio=ratio, amount=amount, keep_id=keep_id)
		else:
			return self.darken(ratio=ratio, amount=amount, keep_id=keep_id)

	def blacken_or_whiten(self) -> 'Colour':
		"""
		Returns the farthest gray colour.

		Returns:
			Colour: The farthest gray Colour object.
		"""
		return self.farthest_gray

	brighten = lighten

	def increase_hue(self, amount: float = DEFAULT_INCREASE_AMOUNT, keep_id: bool = False) -> 'Colour':
		"""
		Increases the hue of the colour.

		Args:
			amount: The amount to increase the hue.
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The resulting Colour object.
		"""
		changed = self.copy(keep_id=keep_id)
		changed.hue = changed.hue + amount
		return changed

	@property
	def farthest_gray(self) -> 'Colour':
		"""
		Returns the farthest gray colour.

		Returns:
			Colour: The farthest gray Colour object.
		"""
		if self.lightness < 0.5:
			return self.__class__(hexadecimal='#FFFFFF', weight=self._weight)
		else:
			return self.__class__(hexadecimal='#000000', weight=self._weight)

	@property
	def nearest_gray(self, keep_id: bool = False) -> 'Colour':
		"""
		Returns the nearest gray colour.

		Args:
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The nearest gray Colour object.
		"""
		gray = self.copy(keep_id=keep_id)
		gray.saturation = 0
		return gray

	@property
	def nearest_red(self, keep_id: bool = False) -> 'Colour':
		"""
		Returns the nearest red colour.

		Args:
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The nearest red Colour object.
		"""
		red = self.copy(keep_id=keep_id)
		red.hue = 0
		return red

	@property
	def nearest_green(self, keep_id: bool = False) -> 'Colour':
		"""
		Returns the nearest green colour.

		Args:
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The nearest green Colour object.
		"""
		green = self.copy(keep_id=keep_id)
		green.hue = 1.0/3.0
		return green

	@property
	def nearest_blue(self, keep_id: bool = False) -> 'Colour':
		"""
		Returns the nearest blue colour.

		Args:
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The nearest blue Colour object.
		"""
		blue = self.copy(keep_id=keep_id)
		blue.hue = 2.0/3.0
		return blue

	def reverse_lightness(self, keep_id: bool = True) -> 'Colour':
		"""
		Reverses the lightness of the colour.

		Args:
			keep_id: Whether to keep the identifier.

		Returns:
			Colour: The resulting Colour object.
		"""
		_reversed = self.copy(keep_id=keep_id)
		_reversed.lightness = 1 - _reversed.lightness
		return _reversed

	def invert(self) -> 'Colour':
		"""
		Inverts the colour.

		Returns:
			Colour: The inverted Colour object.
		"""
		result = self.__class__(red=1 - self.red, green=1 - self.green, blue=1 - self.blue)
		return result

	def mix(self: 'Colour | None' = None, colours: list['Colour'] | None = None) -> 'Colour':
		"""
		Mixes the colour with other colours.

		Args:
			colours: The other Colour objects.

		Returns:
			Colour: The resulting Colour object.
		"""
		if isinstance(colours, (list, tuple)) and len(colours) == 0:
			colours = None
		if colours is None:
			return self.copy(keep_id=True)
		else:
			if isinstance(colours, Colour):
				colours = [colours]

		if self is not None:
			colours = [self] + colours

		red = green = blue = lightness = saturation = 0.0
		id = colours[0].id
		scheme = colours[0].scheme
		for colour in colours:
			red += colour.red * colour._weight
			green += colour.green * colour._weight
			blue += colour.blue * colour._weight
			#lightness += colour.lightness * colour._weight
			#saturation += colour.saturation * colour._weight
			if id != colour.id:
				id = None
				scheme = None

		total_weight = sum([colour._weight for colour in colours])
		red = red / total_weight
		green = green / total_weight
		blue = blue / total_weight
		#lightness = lightness / total_weight
		#saturation = saturation / total_weight
		if self is not None:
			result = self.__class__(
				red=red, green=green, blue=blue, min_value=0.0, max_value=1.0, id=id, scheme=scheme,
				weight=total_weight
			)
		else:
			result = Colour(
				red=red, green=green, blue=blue, min_value=0.0, max_value=1.0, id=id, scheme=scheme,
				weight=total_weight
			)

		#result.set_lightness_and_saturation(lightness=lightness, saturation=saturation)
		return result

	@property
	def weight(self) -> float:
		"""
		Returns the weight of the colour.

		Returns:
			float: The weight.
		"""
		return self._weight

	@weight.setter
	def weight(self, weight: float):
		"""
		Sets the weight of the colour.

		Args:
			weight: The weight.
		"""
		self._weight = weight

	def __eq__(self, other: 'Colour') -> bool:
		"""
		Checks if this colour is equal to another.

		Args:
			other: The other Colour object.

		Returns:
			bool: True if equal, False otherwise.
		"""
		if isinstance(other, (list, tuple)):
			if len(other) != 3:
				raise ValueError(f'other should be a tuple/list of 3 values but it is {other}')
			else:
				other = self.__class__(red=other[0], green=other[1], blue=other[2])

		if not isinstance(other, self.__class__):
			other = self.__class__(obj=other)
		return self.hexadecimal == other.hexadecimal

	def __hash__(self) -> int:
		"""Returns the hash of the colour."""
		return hash(self.hexadecimal)
