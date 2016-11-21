import paho.mqtt.client as mqtt
import json

from led_pixels import pixel_states
from colors import rgb_int_to_tuple
from constants import ZONES, STATE_TOPIC_SUFFIX
from control import get_steps, get_instructions_to_fade_from_middle
from led_pixels import strip
from control import get_range_from_middle
from colors import int_from_rgbw


def on_connect(client, userdata, rc):
    print "Connected.  %s %s %s" % (client, userdata, rc)
    client.subscribe("bedroom/neopixel1/set")
    client.subscribe("kitchen/neopixel1/set")
    client.subscribe("doorway/neopixel1/set")


def on_message(client, userdata, msg):
    print msg.payload
    message = json.loads(msg.payload)

    zone_name = msg.topic.split('/')[0]
    zone = ZONES[zone_name]
    inside_out = get_range_from_middle(zone.range)

    try:
        rgb_dict = message['color']
        new_color = (rgb_dict['r'], rgb_dict['g'], rgb_dict['b'])
    except KeyError:
        new_color = False

    try:
        state = message['state']
        if state == "OFF":
            instruction_set = get_instructions_to_fade_from_middle(inside_out, starting_color=(0, 0, 0), ending_color=(0, 0, 0))
        if state == "ON" and not new_color:  # ie, we're just turning on, no color directive
            # ... we'll do a default color.  TODO: Match with flux.
            new_color = (100, 100, 100)
        if new_color:
            print "Starting from zone current color: %s" % str(zone.current_color)
            instruction_set = get_instructions_to_fade_from_middle(inside_out, starting_color=zone.current_color, ending_color=new_color)
            zone.current_color = new_color

        for instruction_dict in instruction_set:
            for pixel, color in instruction_dict.items():
                rgb_int = int_from_rgbw(*color)
                strip.setPixelColor(pixel, rgb_int)
            strip.show()


        print "Responding to state request; turning %s" % state
        client.publish(msg.topic.replace("/set", "/state"), json.dumps({'state': state}))
    except KeyError:
        pass

    try:
        brightness = message['brightness']
        strip.setBrightness(brightness)
    except KeyError:
        pass

    strip.show()
    announce_all_rgb_states()


def announce_all_rgb_states():
    for zone_name, zone in ZONES.items():
        zone_range = zone.range
        zone_is_homogenous = True

        first_led_in_zone = zone_range[0]
        first_color_int = pixel_states[first_led_in_zone]
        r, g, b = rgb_int_to_tuple(first_color_int)

        announcement = json.dumps({
                           "state" : "ON" if first_color_int else "OFF",
                           "color" : {
                               "g" : g,
                               "r" : r,
                               "b" : b
                           }
                       })

        print "Announcing to %s: %s" % (zone_name + STATE_TOPIC_SUFFIX, announcement)
        client.publish(zone_name + STATE_TOPIC_SUFFIX, payload=announcement, retain=True)

        for led in range(*zone_range):
            if pixel_states[led] != pixel_states[zone_range[0]]:
                zone_is_homogenous = False

        if not zone_is_homogenous:
            print "Zone wasn't homogenous.  What do we do now?"

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message