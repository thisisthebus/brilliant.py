import unittest
from constants import LED_COUNT
from control import get_range_from_middle
from control import get_instructions_to_fade_from_middle


class PixelOrderTests(unittest.TestCase):

    def test_fade_in_same_number_of_steps_each_color(self):
        pixel_range = (41, 125)
        pixel_range_from_middle = get_range_from_middle(pixel_range)
        red_instruction_set = get_instructions_to_fade_from_middle(pixel_range_from_middle, starting_color=(0, 0, 0), ending_color=(200, 0, 0))

        green_instruction_set = get_instructions_to_fade_from_middle(pixel_range_from_middle, starting_color=(0, 0, 0),
                                                                   ending_color=(0, 200, 0))

        blue_instruction_set = get_instructions_to_fade_from_middle(pixel_range_from_middle, starting_color=(0, 0, 0),
                                                                   ending_color=(0, 0, 200))
        self.assertEqual(len(red_instruction_set), len(green_instruction_set))
        self.assertEqual(len(green_instruction_set), len(blue_instruction_set))

    def test_every_pixel_moves_in_correct_direction(self):
        '''
        Had an issue in which some pixels were reverting.  Let's make sure they move the right way.
        '''
        pixel_range = (84, 210)
        starting_color = (117, 108, 255)
        ending_color = (249, 46, 0)
        pixel_range_from_middle = get_range_from_middle(pixel_range)
        instruction_set = get_instructions_to_fade_from_middle(pixel_range_from_middle, starting_color=starting_color,
                                                                   ending_color=ending_color)
        pixel_120_red_color_at_round_60 = instruction_set[60][120][0]
        pixel_120_red_color_at_round_62 = instruction_set[62][120][0]

        self.assertGreater(pixel_120_red_color_at_round_62, pixel_120_red_color_at_round_60)


