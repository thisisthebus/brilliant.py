from constants import OFF
import random


def get_steps(end, begin=0, number_of_steps=None):
    if end == begin == 0:
        return [0]
    if not number_of_steps:
        number_of_steps = end - begin

    return [begin + x * (end - begin) / number_of_steps for x in range(number_of_steps)]


def get_range_from_middle(pixel_range):
    first = pixel_range[0]
    second = pixel_range[1]
    if second < first:
        pixel_list = range(first-1, second-1, -1)
    else:
        pixel_list = range(*pixel_range)
    # From here: https://stackoverflow.com/questions/36533553/cycle-a-list-from-alternating-sides/36533624
    outside_in = [pixel_list[-i // 2] if i % 2 else pixel_list[i // 2] for i in range(len(pixel_list))]
    # OK, but now we're working from the outside; we want from the middle.
    outside_in.reverse()
    # random.shuffle(outside_in)
    return outside_in  # Although it's now inside out.


def get_instructions_to_fade_from_middle(middle_sorted_pixel_range,
                                         ending_color,
                                         starting_color=OFF,
                                         min_round_size=1,
                                         max_round_size=30,
                                         initial_divisor=5):

    instruction_set = []

    pixels_left_to_fade = list(middle_sorted_pixel_range)

    # A tuple of three bools to tell us which channels are decreasing.
    decreasing = map(lambda start, end: start > end, starting_color, ending_color)

    round_size = min_round_size
    latest_pixel_colors = {}
    while pixels_left_to_fade:
        round_instructions = {}
        divisor = initial_divisor

        for step, pixel in enumerate(pixels_left_to_fade):
            if step == round_size:
                break

            # Get the last known color of this pixel.  If we've never set it, it must be the starting_color.
            last_color = latest_pixel_colors.get(pixel, starting_color)

            next_color = []

            for last_channel, starting_channel, ending_channel, channel_is_decreasing in zip(last_color, starting_color, ending_color, decreasing):

                if last_channel == ending_channel:
                    next_channel = last_channel  # If this channel is already consistent with the ending_color, stay where we are.
                else:
                    move = int(abs(ending_channel - starting_channel) / divisor)

                    # We generally don't want to move zero; otherwise we risk being stuck in an infinite loop.
                    move = max(move, 1)

                    next_channel = last_channel - move if channel_is_decreasing else last_channel + move

                    # If we have gone past the end...
                    if (channel_is_decreasing and next_channel < ending_channel) or (not channel_is_decreasing and next_channel > ending_channel):
                        next_channel = ending_channel  #...then just set our next value to the ending value.

                next_color.append(next_channel)

            # Make next_color a tuple (instead of a list) for comparison purposes.
            next_color = tuple(next_color)

            if next_color == ending_color:
                pixels_left_to_fade.remove(pixel)
                round_size = min(round_size, len(pixels_left_to_fade)-1) # Otherwise we won't have enough pixels to loop through next time!
            round_instructions[pixel] = latest_pixel_colors[pixel] = next_color
            divisor += initial_divisor
        instruction_set.append(round_instructions)
        round_size = min(round_size + 1, max_round_size)

    print "From %s to %s with %s instructions" % (starting_color, ending_color, len(instruction_set))
    return instruction_set









