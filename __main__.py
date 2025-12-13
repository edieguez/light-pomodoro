#! /usr/bin/env python3
import json
import time
import tinytuya

d = tinytuya.BulbDevice(
    dev_id='DEVICE_ID',
    address='DEVICE_IP_ADDRESS',
    local_key='DEVICE_LOCAL_KEY',
    version=3.4
)

# get status
status = d.status()
print(f'Table lamp status:\n{json.dumps(status, indent=4)}')

d.turn_on()

# Cycle through the Rainbow
rainbow = {"red": [255, 0, 0], "orange": [255, 127, 0], "yellow": [255, 200, 0],
          "green": [0, 255, 0], "blue": [0, 0, 255], "indigo": [46, 43, 95],
          "violet": [139, 0, 255]}

for color in rainbow.items():
    [r, g, b] = color[1]
    d.set_colour(r, g, b, nowait=True)  # nowait = Go fast don't wait for response
    time.sleep(0.25)
