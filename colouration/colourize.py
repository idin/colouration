RESET = '\033[0m'


def get_color_escape(r, g, b, background=False):
	return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


def colourize(string, red, green, blue, bg_red=None, bg_green=None, bg_blue=None):
	red = max(0.0, min(1.0, red))
	green = max(0.0, min(1.0, green))
	blue = max(0.0, min(1.0, blue))
	red, green, blue = int(red*255), int(green*255), int(blue*255)
	if bg_red is None or bg_green is None or bg_blue is None:
		return get_color_escape(red, green, blue) + string + RESET

	bg_red = max(0.0, min(1.0, bg_red))
	bg_green = max(0.0, min(1.0, bg_green))
	bg_blue = max(0.0, min(1.0, bg_blue))
	bg_red, bg_green, bg_blue = int(bg_red * 255), int(bg_green * 255), int(bg_blue * 255)
	return get_color_escape(red, green, blue) + get_color_escape(bg_red, bg_blue, bg_green, True) + string + RESET
