RESET = '\033[0m'


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    return tuple(int(hex_str[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return '%02x%02x%02x' % rgb


def get_color_escape(dec: tuple[float, float, float], background=False):
    r, g, b = dec
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)


def rgb_to_hsv(rgb: tuple[int, int, int]):
    """ 
    Converts an rgb tuple to hsv	
    """
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
        saturation = round((1 - minColor / maxColor), 2)
    else:
        saturation = 0

    return hue, saturation, value


def hsv_to_rgb(hsv: tuple[float, float, float]) -> tuple[int, int, int]:
    h, s, v = hsv
    M = 255 * v
    m = M * (1 - s)

    z = (M - m) * (1 - abs((h / 60) % 2 - 1))
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


def get_accents(base_color: tuple[float, float, float]) -> tuple[
    list[tuple[float, float, float]], list[tuple[int, int, int]]]:
    _hsv_colors = [(0, 0, 0) for i in range(0, 9)]  # type: list[tuple[float, float, float]]
    _hsv_colors[4] = base_color
    for i in range(0, 9):
        if i < 5:
            if _hsv_colors[i] is None:
                _hsv_colors[i] = [base_color[0], 0.2 + (abs(base_color[1] - 0.2) / 5) * (i + 1),
                                  1 - (abs(base_color[2] - 1) / 5) * (i + 1)]
        else:
            if _hsv_colors[-abs(i - 4)] is None:
                _hsv_colors[-abs(i - 4)] = [base_color[0], 1 - (abs(base_color[1] - 1) / 4) * abs(i - 5),
                                            0.4 + (abs(base_color[2] - 0.4) / 4) * (i - 5)]
    _rgb_colors = [hsv_to_rgb(rgb_t) for rgb_t in _hsv_colors if rgb_t is not None]

    return _hsv_colors, _rgb_colors


def modify_angle(base_color: tuple[float, float, float], angle: int):
    new_hsv = (angle, base_color[1], base_color[2])  # type: tuple[float, float, float]
    return get_accents(new_hsv)


def print_a_color(hsv: tuple[float, float, float]):
    rgb = hsv_to_rgb(hsv)
    print(f"{get_color_escape(rgb, True)}           {RESET} ({hsv}) => ({rgb_to_hex(rgb)})")


def print_colors(rgb_list: list[tuple[int, int, int]]):
    """ 
    Prints a list of colors
    
    Attributes:
    ---------
    rgb_list: a list of rgb tuples only
    """
    for index, color in enumerate(rgb_list):
        print(f"{get_color_escape(color, True)}           {RESET} => ({rgb_to_hex(color)})")


def get_complementer(hsv: tuple[float, float, float], hue_diff: float, saturation_diff: float, value_diff: float) -> \
        tuple[float, float, float]:
    """ Returns the complementer `hsv` tuple """

    h, s, v = hsv
    return ((h + hue_diff) % 360, s + saturation_diff, v + value_diff)


def get_css_format(list_of_colors: tuple[int, int, int], var_name: str) -> list[str]:
    str_list = []
    for i, c in enumerate(list_of_colors):
        color_str = f'--{var_name}-{i + 1}: {rgb_to_hex(c)}'
        str_list.append(color_str)
        print(color_str)
    return str_list
