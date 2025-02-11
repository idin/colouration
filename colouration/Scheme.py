from .colour_schemes import colour_schemes
from .Colour import Colour, DEFAULT_INCREASE_RATIO


DEFAULT_SCHEME_NAME = 'pastel19'

ADDITIONAL_SCHEMES = {
	'pensieve': ['#fbb4ae', '#ccebc5', '#decbe4', '#fed9a6', '#fff2ae', '#e5d8bd', '#fddaec'],
	'pensieve2': [
		'#8dd3c7', '#bebada', '#fb8072', '#80b1d3', '#fdb462', '#b3de69', '#fccde5', '#bc80bd', '#ccebc5', '#ffed6f'
	]
}


class Scheme:
	def __init__(self, colours=None, name=DEFAULT_SCHEME_NAME, normalize_lightness=0.5):
		"""
		Initializes a Scheme object.

		Args:
			colours: List of Colour objects.
			name: Name of the scheme.
			normalize_lightness: Lightness normalization factor.
		"""
		if colours is None and name.lower() in ADDITIONAL_SCHEMES:
			colours = [Colour(hexadecimal=hex) for hex in ADDITIONAL_SCHEMES[name]]
		else:
			colours = colours or [Colour(hexadecimal=hex) for hex in colour_schemes[name.lower()]]

		if normalize_lightness is not None:
			mean_lightness = sum([colour.lightness for colour in colours]) / len(colours)
			mean_lightness = mean_lightness + (1 - mean_lightness) * normalize_lightness
			for colour in colours:
				colour.lightness = mean_lightness

		self._colours = {}
		self._colour_usages = {}
		self._usage_logs = {}
		self._set_colours(colours)
		self._name = name

	def _set_colours(self, colours):
		"""Sets the colours for the scheme."""
		for colour_id, colour in enumerate(colours):
			try:
				colour_original_id = colour.id
			except AttributeError:
				colour_original_id = None
			self._colours[colour_id] = Colour(obj=colour, id=colour_original_id or colour_id, scheme=self)
			if colour_id not in self._colour_usages:
				self._colour_usages[colour_id] = 0
			self._usage_logs[colour_id] = []

	def __getstate__(self):
		"""Returns the state of the scheme for pickling."""
		return {
			'colours': [colour.__getstate__() for colour in self.colours],
			'colour_usages': self._colour_usages,
			'usage_logs': self._usage_logs,
			'name': self._name
		}

	def __setstate__(self, state):
		"""Sets the state of the scheme from pickling."""
		self._colour_usages = state['colour_usages']
		self._usage_logs = state['usage_logs']
		self._name = state['name']
		self._set_colours(colours=[Colour._from_state(colour_state) for colour_state in state['colours']])

	@property
	def num_colours(self):
		"""Returns the number of colours in the scheme."""
		return len(self.colours)

	def pick_by_index(self, index: int) -> Colour:
		"""
		Picks a colour by index.

		Args:
			index: The index of the colour.

		Returns:
			Colour: The Colour object.
		"""
		return self._colours[index % self.num_colours]

	@property
	def colours_in_order_of_usage(self):
		"""Returns the colours in order of usage."""
		return sorted(self.colours, key=lambda x: (x.usage, x.id))

	@property
	def least_used_colour(self):
		"""Returns the least used colour."""
		return self.colours_in_order_of_usage[0]

	@property
	def logs(self):
		"""Returns the usage logs of the scheme."""
		return [
			{'id': colour.id, 'colour': colour, 'usage': colour.usage, 'logs': colour.logs}
			for colour in self._colours.values()
		]

	def use(self, colour: Colour, log=None):
		"""
		Logs the usage of a colour in the scheme.

		Args:
			colour: The Colour object.
			log: Optional log information.
		"""
		self._colour_usages[colour.id] += 1
		if log is not None:
			self._usage_logs[colour.id].append(log)

	def get_usage(self, colour: Colour) -> int:
		"""
		Returns the usage count of a colour.

		Args:
			colour: The Colour object.

		Returns:
			int: The usage count.
		"""
		return self._colour_usages[colour.id]

	def copy(self):
		"""Creates a copy of the scheme."""
		return self.__class__(colours=[colour.copy() for colour in self.colours], name=self._name)

	@property
	def _max_name_length(self):
		"""Returns the maximum name length of the colours."""
		return max([len(colour.name) for colour in self.colours]) + 2

	@property
	def colours(self):
		"""
		Returns the list of colours in the scheme.

		Returns:
			list[Colour]: The list of colours.
		"""
		if any([c is None for c in self._colours]):
			for c in self._colours:
				print(c)
			raise TypeError('colour is None!')
		return [self._colours[i] for i in range(len(self._colours))]

	def display(self, main_colour='background'):
		"""
		Displays the scheme.

		Args:
			main_colour: The main colour for display.
		"""
		for colour in self.colours:
			name = colour.name.ljust(self._max_name_length)
			hue = str(round(colour.hue, 3)).ljust(5, '0')
			sat = str(round(colour.saturation, 3)).ljust(5, '0')
			lig = str(round(colour.lightness, 3)).ljust(5, '0')
			string = f'  h:{hue} s:{sat} l:{lig} '
			string = string.rjust(25)
			colour.display(
				string=' ' + name + string,
				length=self._max_name_length + 26,
				main_colour=main_colour
			)

	def adjust(self, hue=None, saturation=None, lightness=None):
		"""
		Adjusts the hue, saturation, and lightness of the scheme.

		Args:
			hue: The hue adjustment.
			saturation: The saturation adjustment.
			lightness: The lightness adjustment.

		Returns:
			Scheme: The adjusted Scheme object.
		"""
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
		"""
		Increases the hue, saturation, and lightness of the scheme.

		Args:
			hue: The hue increase.
			saturation: The saturation increase.
			lightness: The lightness increase.

		Returns:
			Scheme: The increased Scheme object.
		"""
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
		Inverts the scheme.

		Returns:
			Scheme: The inverted Scheme object.
		"""
		return self.__class__(colours=[~colour for colour in self.colours])

	def __invert__(self):
		"""
		Inverts the scheme.

		Returns:
			Scheme: The inverted Scheme object.
		"""
		return self.invert()

	def darken(self, ratio=0.5):
		"""
		Darkens the scheme.

		Args:
			ratio: The ratio to darken.

		Returns:
			Scheme: The darkened Scheme object.
		"""
		return self.__class__(colours=[colour.darken(ratio=ratio) for colour in self.colours])

	def lighten(self, ratio=0.5):
		"""
		Lightens the scheme.

		Args:
			ratio: The ratio to lighten.

		Returns:
			Scheme: The lightened Scheme object.
		"""
		return self.__class__(colours=[colour.lighten(ratio=ratio) for colour in self.colours])

	brighten = lighten

	def darken_or_lighten(self, ratio=DEFAULT_INCREASE_RATIO):
		"""
		Darkens or lightens the scheme based on the lightness.

		Args:
			ratio: The ratio to adjust.

		Returns:
			Scheme: The adjusted Scheme object.
		"""
		return self.__class__(colours=[colour.darken_or_lighten(ratio=ratio) for colour in self.colours])

	@property
	def blacken_or_whiten(self):
		"""
		Returns the farthest gray scheme.

		Returns:
			Scheme: The farthest gray Scheme object.
		"""
		return self.__class__(colours=[colour.blacken_or_whiten for colour in self.colours])

	@property
	def farthest_gray(self):
		"""
		Returns the farthest gray scheme.

		Returns:
			Scheme: The farthest gray Scheme object.
		"""
		return self.__class__(colours=[colour.farthest_gray for colour in self.colours])

	@property
	def nearest_gray(self):
		"""
		Returns the nearest gray scheme.

		Returns:
			Scheme: The nearest gray Scheme object.
		"""
		return self.__class__(colours=[colour.nearest_gray for colour in self.colours])

	@property
	def nearest_red(self):
		"""
		Returns the nearest red scheme.

		Returns:
			Scheme: The nearest red Scheme object.
		"""
		return self.__class__(colours=[colour.nearest_red for colour in self.colours])

	@property
	def nearest_green(self):
		"""
		Returns the nearest green scheme.

		Returns:
			Scheme: The nearest green Scheme object.
		"""
		return self.__class__(colours=[colour.nearest_green for colour in self.colours])

	@property
	def nearest_blue(self):
		"""
		Returns the nearest blue scheme.

		Returns:
			Scheme: The nearest blue Scheme object.
		"""
		return self.__class__(colours=[colour.nearest_blue for colour in self.colours])
