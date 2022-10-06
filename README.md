# GranTurismo
This package wraps the Gran Turismo 7's unofficial telemetry API. By providing this module with you're PlayStation's IP address (as found in the menu) you will be able to retrieve packets containing telemetry data. 

## Data
Because this is an unofficial API, the range expected min/max of each value is still unknown. As more effort is put into understanding this API, better information will be available. For now, here is what we know.
*  int: `  packet_id`
*  int: `  car_id`
*  int or None: `lap_count`
*  int or None: `laps_in_race`
*  int or None: `best_lap_time`
*  int or None: `last_lap_time`
*  Vector: `position`
   * float: `x`
   * float: `y`
   * float: `z` 
*  Vector: `velocity`
   * float: `x`
   * float: `y`
   * float: `z` 
*  Vector: `angular_velocity`
   * float: `x`
   * float: `y`
   * float: `z` 
*  Rotation: `rotation`
   * float: `pitch`
   * float: `yaw`
   * float: `roll` 
*  Vector: `road_plane`
   * float: `x`
   * float: `y`
   * float: `z` 
*  float: `road_distance`: Should match the `body_height` when car is on the ground
*  Wheels: `wheels`
   * Wheel: `front_left`
     * float: `suspension_height`: between 0-1. Lower number equates to uncompressed, higher number to a more compressed suspension
     * float: `radius`: Radius of the tire in meters 
     * float: `rps`: Rotations per second 
     * float: `ground_speed`: The speed the tire is traveling on the ground in meters per second. 
     * float: `temperature`: The surface temperature of the tire in celsius 
   * Wheel: `y`
       * float: `suspension_height`: between 0-1. Lower number equates to uncompressed, higher number to a more compressed suspension
       * float: `radius`: Radius of the tire in meters
       * float: `rps`: Rotations per second
       * float: `ground_speed`: The speed the tire is traveling on the ground in meters per second.
       * float: `temperature`: The surface temperature of the tire in celsius 
   * Wheel: `z` 
       * float: `suspension_height`: between 0-1. Lower number equates to uncompressed, higher number to a more compressed suspension
       * float: `radius`: Radius of the tire in meters
       * float: `rps`: Rotations per second
       * float: `ground_speed`: The speed the tire is traveling on the ground in meters per second.
       * float: `temperature`: The surface temperature of the tire in celsius 
   * Wheel: `x`
       * float: `suspension_height`: between 0-1. Lower number equates to uncompressed, higher number to a more compressed suspension
       * float: `radius`: Radius of the tire in meters
       * float: `rps`: Rotations per second
       * float: `ground_speed`: The speed the tire is traveling on the ground in meters per second.
       * float: `temperature`: The surface temperature of the tire in celsius 
*  Flags: `flags`
*  float: `orientation`
*  float: `body_height` in meters
*  float: `engine_rpm`
*  float: `gas_level`
*  float: `gas_capacity` 100 for gas cars, 5 for karts, 0 for electric
*  float: `car_speed` in meters per second
*  float: `turbo_boost`
*  float: `oil_pressure` in bars?
*  float: `oil_temperature` in celsius
*  float: `water_temperature` in celsius
*  int: `time_of_day` in seconds since midnight
*  Optional(int): `start_position` only available before race starts, otherwise None
*  Optional(int): `cars_in_race` only available before race starts, otherwise None
*  Bounds: `rpm_alert`
   * float: `min`
   * float: `max`
*  int:  `car_max_speed` in meters per second
*  float: `transmission_max_speed` in terms of gear ratio? 
*  int: `throttle` between 0-255
*  int: `brake` between 0-255
*  float: `clutch` between 0-1. This seems to correlate with the clutch peddle
*  float: `clutch_engagement` between 0-1
*  float: `clutch_gearbox_rpm`
*  int: `current_gear`
*  Optional(int): `suggested_gear`. None if there's no suggested gear
*  List(float): `gear_ratios` 1st - Nth gear. 
*  int: `unused_0x93`
*  int: `unused_0xD4`

## Installation
To install, run `pip install granturismo`

## Usage
The main function is the Listener, which is a closing object. You can use a `with Listener(ip_address) as ...` clause to open and close the listener. 
The Listener will spin up a background thread to maintain a heartbeat connection with the PlayStation, so it's important to always close the object.

### Quickstart example
Grab a single packet from Gran Turismo and print it
```python
from granturismo.intake import Listener
import sys

if __name__ == '__main__':
  ip_address = sys.argv[1]
  with Listener(ip_address) as listener:
    print(listener.get())
```

### Streaming data example
Stream all incoming data from Gran Turismo and print it to the terminal
```python
import sys

from granturismo.intake import Listener
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
  ip_address = sys.argv[1]

  # setup the plot styling
  plt.ion()
  fig = plt.figure(figsize=(10, 10))
  plt.xticks([])
  plt.yticks([])

  px, pz = None, None

  prev_time = 0
  with Listener(ip_address) as listener:
    curr_time = time.time()

    # only update graph every 10th of a second just cuz it doesn't matter for us, and it's easier on the computer
    if curr_time - prev_time > 0.1:
      packet = listener.get()

      # note, we're negating z so the map will appear int he same orientation as it does in the game's minimap
      x, z = packet.position.x, -packet.position.z

      if px is not None:
        # here we're adding 3 points on top of each other so that the final point will have the correct coloring for the car's speed range.
        # we're plotting (min speed, max speed, current speed) and matplotlib will adjust the color map so that the final (current speed)
        # color is accurate
        plt.plot([px, x], [pz, z], s=1)

        # pause for a freakishly shot amount of time. We need a pause so that it'll trigger a graph update
        plt.pause(0.00001)

      px, pz = x, z
```