from colorlib import *

primary = input("Enter a hex color: ") or "ff00c1"
if primary[0] == "#":
	primary = primary[1:]

rgb = hex_to_rgb(primary)
o_hsv = rgb_to_hsv(rgb)

comp1 = get_complementer(o_hsv, 150, 0, 0)
comp1_s = get_complementer(o_hsv, 150, -0.07, -0.3)
comp2 = get_complementer(o_hsv, 210, 0, 0)
comp2_s = get_complementer(o_hsv, 210, -0.07, -0.3)

print_colors(get_accents(rgb_to_hsv(rgb)))
get_css_format(get_accents(rgb_to_hsv(rgb))[1], "primary")
# print_colors(modify_angle(rgb_to_hsv(rgb), 5))
# print_colors(modify_angle(rgb_to_hsv(rgb), 55))
# print_colors(modify_angle(rgb_to_hsv(rgb), 100))
# print_colors(modify_angle(rgb_to_hsv(rgb), 200))
# print()

# print_a_color(o_hsv)
# print_a_color(comp1)
# print_a_color(comp1_s)
# print_a_color(comp2)
# print_a_color(comp2_s)



