import colorsys
import math

RESET = '\033[0m'

def hex_to_rgb(hex_str: str) -> tuple:
	return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

def get_color_escape(dec: tuple, background=False):
    r, g, b = dec
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def rgb_to_hsv(rgb):
	red, green, blue = rgb
	maxColor = max(rgb)
	minColor = min(rgb)

	if red == green == blue:
		hue = 0
	elif maxColor == red:
		hue = (green - blue) / (maxColor - minColor)
	elif maxColor == green:
		hue = 2.0 + (blue - red) / (maxColor - minColor)
	elif maxColor == blue:
		hue = 4.0 + (red - green) / (maxColor - minColor)

	hue *= 60

	if hue < 0:
		hue += 360
	hue = round(hue, 2)
	value = round(maxColor / 255, 2)

	if maxColor > 0:
		saturation = round((1 - minColor/maxColor), 2)
	else:
		saturation = 0

	return hue, saturation, value

def hsv_to_rgb(hsv):
	h, s, v = hsv
	M = 255 * v
	m = M * (1 - s)

	z = (M - m) * (1 - abs((h/60) % 2 - 1))
	if 0 <= h < 60:
		r = M
		g = z + m
		b = m
	elif 60 <= h < 120:
		r = z + m
		g = M
		b = m
	elif 120 <= h < 180:
		r = m
		g = M
		b = z + m
	elif 180 <= h < 240:
		r = m
		g = z + m
		b = M
	elif 240 <= h < 300:
		r = z + m
		g = m
		b = M
	elif 300 <= h < 360:
		r = M
		g = m
		b = z + m

	return int(round(r)), int(round(g)), int(round(b))

def get_accents(base_color):
	_hsv_colors = [None for i in range(0, 9)]
	_hsv_colors[4] = base_color
	for i in range(0, 9):
		if i < 5:
			if _hsv_colors[i] is None:
				_hsv_colors[i] = [base_color[0], 0.2 + (abs(base_color[1] - 0.2) / 5) * (i + 1), 1 - (abs(base_color[2] - 1) / 5) * (i + 1)]
		else:
			if _hsv_colors[-abs(i - 4)] is None:
				_hsv_colors[-abs(i - 4)] = [base_color[0], 1 - (abs(base_color[1] - 1) / 4) * abs(i - 5), 0.4 + (abs(base_color[2] - 0.4) / 4) * (i - 5)]
	_rgb_colors = [hsv_to_rgb(rgb_t) for rgb_t in _hsv_colors if rgb_t is not None]
	
	return _hsv_colors, _rgb_colors

def modify_angle(base_color, angle):
	new_hsv = [angle, base_color[1], base_color[2]]
	return get_accents(new_hsv)

def print_a_color(hsv):
	rgb = hsv_to_rgb(hsv)
	print(f"{get_color_escape(rgb, True)}           {RESET} ({hsv}) => ({rgb_to_hex(rgb)})")

def print_colors(list_tuple):
	hsv_list = list_tuple[0]
	rgb_list = list_tuple[1]
	for index, color in enumerate(rgb_list):
		print(f"{get_color_escape(color, True)}           {RESET} ({hsv_list[index]}) => ({rgb_to_hex(color)})")

def get_complementer(hsv, hue_diff, saturation_diff, value_diff):
	h, s, v = hsv
	return ((h + hue_diff) % 360, s + saturation_diff, v + value_diff)


primary = input("Enter a hex color: ") or "ff00c1"
if primary[0] == "#":
	primary = primary[1:]

rgb = hex_to_rgb(primary)
o_hsv = rgb_to_hsv(rgb)

comp1 = get_complementer(o_hsv, 100, 0, 0)
comp1_s = get_complementer(o_hsv, 100, -0.07, -0.3)
comp2 = get_complementer(o_hsv, 171, 0, 0)
comp2_s = get_complementer(o_hsv, 171, -0.07, -0.3)

print_colors(get_accents(rgb_to_hsv(rgb)))
print_colors(modify_angle(rgb_to_hsv(rgb), 5))
print_colors(modify_angle(rgb_to_hsv(rgb), 55))
print_colors(modify_angle(rgb_to_hsv(rgb), 100))
print_colors(modify_angle(rgb_to_hsv(rgb), 200))
print()

print_a_color(o_hsv)
print_a_color(comp1)
print_a_color(comp1_s)
print_a_color(comp2)
print_a_color(comp2_s)



