def rgb_int_to_tuple(rgb_int):
    b = rgb_int & 255
    r = (rgb_int >> 8) & 255
    g = (rgb_int >> 16) & 255
    return r, g, b


def int_from_rgbw(red, green, blue, white=0):
    return (white << 24) | (green << 16)| (red << 8) | blue