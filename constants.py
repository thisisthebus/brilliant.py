# LED strip configuration:
from zones import Zone

LED_COUNT      = 240      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 225     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

ZONES = {'kitchen': Zone('kitchen', (0, 40)),
         'doorway': Zone('doorway', (40, 84)),
         'bedroom': Zone('bedroom', (84, 210)),
         }

STATE_TOPIC_SUFFIX = "/neopixel1/state"

OFF = (0, 0, 0)
