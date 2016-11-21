from constants import ZONES
from control import get_range_from_middle, get_instructions_to_fade_from_middle
from led_pixels import strip
from colors import int_from_rgbw
from pprint import pprint

starting_color = (255, 61, 47)
ending_color = (2, 0, 244)

inside_out = get_range_from_middle(ZONES['bedroom'].range)


# glitchy going down the strip (144, 4, 0) to (129, 121, 255)
# glitchy going up the strip (117, 108, 255) to (249, 46, 0)
starting_color = (117, 108, 255)
ending_color = (249, 46, 0)

instruction_set = get_instructions_to_fade_from_middle(inside_out, starting_color=starting_color, ending_color=ending_color)
# pprint(instruction_set)

DEBUG = False

for i in inside_out:
    color_int = int_from_rgbw(*starting_color)
    strip.setPixelColor(i, color_int)

for round, instruction_dict in enumerate(instruction_set):
    for pixel, color in instruction_dict.items():

        if DEBUG:
            if pixel == 120:
                print "setting %s to %s for round %s" % (pixel, color, round)
                if tuple(color) == ending_color:
                    print "exiting."
                    exit()

        color_int = int_from_rgbw(*color)
        strip.setPixelColor(pixel, color_int)
    strip.show()


