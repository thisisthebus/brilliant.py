from constants import LED_COUNT
from mqtt_interface import announce_all_rgb_states

from mqtt_interface import client
client.connect("localhost", 1883, 60)

from led_pixels import strip
for i in range(LED_COUNT):
    strip.setPixelColor(i, 0)

strip.show()

announce_all_rgb_states()

client.loop_forever()