def rgb_to_hex(rgb: tuple[int, int, int]):
    return '{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def hex_to_rgb(hex: str):
    return tuple(int(hex.strip('#')[i:i+2], 16) for i in (0, 2, 4))


def int_to_rgb(color: int):
    return (
        (color >> 16) & 255,
        (color >> 8) & 255,
        color & 255
    )


def rgb_to_int(rgb: tuple[int, int, int]):
    red, green, blue = rgb
    return (red << 16) + (green << 8) + blue