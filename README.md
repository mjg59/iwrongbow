iwrongbow is a Python module for controlling iRainbow Zigbee LED bulbs.

Usage:

The discover method will discover a bridge on your local network

bridge = iwrongbow.discover()

To ask the bridge to probe for lights:

bridge.probe()

To ask the bridge for the list of known lights:

lights = bridge.lights()

To set the white intensity of a light (between 0 and 255):

light.set_brightness(128)

To set the RGB value of a light:

light.set_colour(0, 128, 255)