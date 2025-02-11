# *Colouration* 

*Colouration* is a Python library for working with colours. 
It unifies three representation of colour: 
- [RGB](https://en.wikipedia.org/wiki/RGB_color_model) (red, green, blue)
- [HSL](https://en.wikipedia.org/wiki/HSL_and_HSV) (hue, saturation, lightness)
- [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV) (hue, saturation, value)

## Installation
```bash
pip install colouration
```

## Usage

### `Colour`
```python
from colouration import Colour

default_arguments = Colour(
	obj=None,
	red=None, green=None, blue=None, 
	hexadecimal=None,
	hue=None, saturation=None, lightness=None, value=None,
	min_value=0.0, max_value=1.0, 
	name=None, id=None, scheme=None,
	weight=1.0
)

# you can use the rgb hexadecimal code to create a Colour object
red = Colour('#FF0000')

# you can enter red, green, and blue as separate values
green = Colour(red=0, green=1, blue=0)

# max value is 1 by default but other values can be used too
blue = Colour(red=0, green=0, blue=255, max_value=255)

# and you can use colour names 
literal_red = Colour('red')
print(f'is red equal to literal_red? {"yes" if red == literal_red else "no"}\n')

# you can print with it
literal_red.print('by default the main colour is used for background\n')

# to use the colour as the text colour you should use the main_colour argument
red.print(string='red text\n', main_colour='text', secondary='auto') # secondary='auto' is default

# the secondary colour is white when the main colour is dark and it is black otherwise
red.print(string='the secondary colour is white when the main colour is dark and it is black otherwise.\n')

# you can choose a secondary colour
red.print(string='red on white\n', main_colour='text', secondary='white')

# you can use string or a Colour object
red.print(string='blue on red\n', secondary=Colour('blue'))

# you can darken or lighten a colour
dark_red = red.darken(ratio=0.5)
dark_red.print(string='dark red\n') 

# ratio can be between 0 and 1
light_red = red.lighten(ratio=0.8) 

# you can change the hue of a colour
new_colour = red.increase_hue(0.2)
new_colour.print('hue increased by 0.2\n')

# you can assign a new hue, lightness, value, red, green, or blue too
new_colour.red = 0.2
new_colour.print('setting red = 0.2 causes this.\n')
new_colour.hue = 0.8
new_colour.print('setting hue = 0.4 causes this.\n')
new_colour.value = 0.3
new_colour.print('setting value = 0.3 causes this.\n')
new_colour.lightness = 0.9
new_colour.print('setting lightness = 0.9 causes this.\n')

# you can mix colours by adding them together
yellow = green + red
yellow.print(string='mixing green and red produces this.\n')

# Colour finds the best name for itself
bluish = Colour(red=220, green=243, blue=255, max_value=255) # max_value is 1 by default
bluish.print(string=f'Colour finds the best name for itself: {bluish.name}.\n')
```

### `Scheme`

### `Gradient`