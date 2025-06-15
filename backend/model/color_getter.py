def hex_to_rgb(hex_color: str) -> tuple:
    """
    Converts a hex color string to an RGB tuple.

    :param hex_color: The color in hex format (e.g., '#ff0000').
    :return: A tuple containing the RGB values (R, G, B) as integers, each in the range 0-255.
    """
    hex_color = hex_color.lstrip('#')  # Remove the '#' if present
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color: tuple) -> str:
    """
    Converts an RGB tuple to a hex color string.

    :param rgb_color: A tuple containing the RGB values (R, G, B) as integers, each in the range 0-255.
    :return: The color in hex format (e.g., '#ff0000').
    """
    return '#' + ''.join(f'{c:02x}' for c in rgb_color)


def interpolate_color(color1: str, color2: str, value: float) -> str:
    """
    Interpolates between two hex colors based on a value between 0 and 1.

    :param color1: The first color in hex format (e.g., '#ff0000').
    :param color2: The second color in hex format (e.g., '#0000ff').
    :param value: A float between 0 and 1 representing the interpolation factor.
    :return: A hex color representing the gradient between the two colors.
    """
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)

    interpolated_rgb = (
        int(rgb1[0] + (rgb2[0] - rgb1[0]) * value),
        int(rgb1[1] + (rgb2[1] - rgb1[1]) * value),
        int(rgb1[2] + (rgb2[2] - rgb1[2]) * value)
    )

    return rgb_to_hex(interpolated_rgb)
