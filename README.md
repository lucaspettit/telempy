# GranTurismo
This package wraps the Gran Turismo 7's unofficial telemetry API. By providing this module with you're PlayStation's IP address (as found in the menu) you will be able to retrieve packets containing telemetry data. 

## Usage
The main function is the Listener, which is a closing object. You can use a `with Listener(ip_address) as ...` clause to open and close the listener. 
The Listener will spin up a background thread to maintain a heartbeat connection with the PlayStation, so it's important to always close the object.

### Quickstart example
Grab a single packet from Gran Turismo and print it
```python
from granturismo.intake import Listener
import sys

if __name__ == '__main__':
  ip_address = sys.argv[1] # IP address to the PlayStation
  
  # Create a new Listener session and print the first packet that Gran Turismo sends.
  with Listener(ip_address) as listener:
    print(listener.get())
```

### Streaming data example
Stream all incoming data from Gran Turismo and print it to the terminal
```python
from granturismo.intake import Listener
from granturismo.model import Wheels
import datetime as dt
import time, sys
import curses

stdscr = curses.initscr()

# This function is used to rewrite multiple lines on the terminal
def report_suspension(wheels: Wheels) -> None:
  pad = ' ' * 100
  curr_time = dt.datetime.fromtimestamp(time.time()).isoformat()
  stdscr.addstr(0, 0, f'[{curr_time}] Suspension Height{pad}')
  stdscr.addstr(1, 0, f'\t{wheels.front_left.suspension_height:.3f}    {wheels.front_right.suspension_height:.3f}{pad}')
  stdscr.addstr(2, 0, f'\t{wheels.rear_left.suspension_height:.3f}    {wheels.rear_right.suspension_height:.3f}{pad}')
  stdscr.refresh()

if __name__ == '__main__':
  ip_address = sys.argv[1]

  # To use the Listener session without a `with` clause, you'll need to call the `.start()` function. 
  listener = Listener(ip_address)
  listener.start()

  try:
    while True:
      # get the latest packet from PlayStation
      packet = listener.get()

      # If the game isn't paused or in a loading state, we'll update the terminal with the latest suspension info.
      if not packet.flags.loading_or_processing and not packet.flags.paused:
        report_suspension(packet.wheels)
  finally:
    # If you don't use a `with` clause, then you'll need to close the session afterwords. Session will also successfully close with CTRL+C
    listener.close()
    curses.echo()
    curses.nocbreak()
    curses.endwin()
```

## Data
Because this is an unofficial API, the range expected min/max of each value is still unknown. As more effort is put into understanding this API, better information will be available. For now, here is what we know.
*  int: `  packet_id`
*  int: `  car_id` cars with more than 8 gears will overwrite this value with a gear ratio
*  Optional(int): `lap_count` None if not in race
*  Optional(int): `laps_in_race` None if not in race
*  Optional(int): `best_lap_time` In milliseconds. None if not in race, or no lap complete. 
*  Optional(int): `last_lap_time` In milliseconds. None if no lap completed
*  Vector: `position`
   * float: `x`
   * float: `y`
   * float: `z` 
*  Vector: `velocity` in meters per second
   * float: `x`
   * float: `y`
   * float: `z` 
*  Vector: `angular_velocity` radians per second
   * float: `x`
   * float: `y`
   * float: `z` 
*  Rotation: `rotation` Seems to be the real part of a unit quaternion that gives the rotation of the car relative to the track coordinate system
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
   * Wheel: `front_right`
       * float: `suspension_height`: between 0-1. Lower number equates to uncompressed, higher number to a more compressed suspension
       * float: `radius`: Radius of the tire in meters
       * float: `rps`: Rotations per second
       * float: `ground_speed`: The speed the tire is traveling on the ground in meters per second.
       * float: `temperature`: The surface temperature of the tire in celsius 
   * Wheel: `rear_left` 
       * float: `suspension_height`: between 0-1. Lower number equates to uncompressed, higher number to a more compressed suspension
       * float: `radius`: Radius of the tire in meters
       * float: `rps`: Rotations per second
       * float: `ground_speed`: The speed the tire is traveling on the ground in meters per second.
       * float: `temperature`: The surface temperature of the tire in celsius 
   * Wheel: `rear_right`
       * float: `suspension_height`: between 0-1. Lower number equates to uncompressed, higher number to a more compressed suspension
       * float: `radius`: Radius of the tire in meters
       * float: `rps`: Rotations per second
       * float: `ground_speed`: The speed the tire is traveling on the ground in meters per second.
       * float: `temperature`: The surface temperature of the tire in celsius 
*  Flags: `flags`
   * bool: `in_race`
   * bool: `paused` 
   * bool: `loading_or_processing` 
   * bool: `in_gear` 0 when shifting or out of gear, standing 
   * bool: `has_turbo` 
   * bool: `rev_limiter_alert_active` 
   * bool: `hand_brake_active` 
   * bool: `lights_active` 
   * bool: `lights_high_beams_active` 
   * bool: `lights_low_beams_active` 
   * bool: `asm_active` 
   * bool: `tcs_active` 
   * bool: `unused1` always False 
   * bool: `unused2` always False 
   * bool: `unused3` always False 
   * bool: `unused4` always False 
*  float: `orientation`
*  float: `body_height` in meters
*  float: `engine_rpm` 0-?
*  float: `gas_level` 0-100
*  float: `gas_capacity` 100 for gas cars, 5 for karts, 0 for electric
*  float: `car_speed` in meters per second
*  float: `turbo_boost` this value - 1 gives the Turbo Boost display
*  float: `oil_pressure` in bars?
*  float: `oil_temperature` in celsius. Seems to always be 85.0
*  float: `water_temperature` in celsius. Seems to always be 110.0
*  int: `time_of_day` millisecond timestamp, time of day indicates race start time of day, affected by Variable Time Speed Ratio, useless for timing when time speed ratio is not 1
*  Optional(int): `start_position` only available before race starts, otherwise None
*  Optional(int): `cars_in_race` only available before race starts, otherwise None
*  Bounds: `rpm_alert`
   * float: `min` 0-?
   * float: `max` 0-?
*  int:  `car_max_speed` in meters per second
*  float: `transmission_max_speed`	corresponds to the Top Speed setting of a customizable gear box in the car settings, given as gear ratio 
*  int: `throttle` between 0-255
*  int: `brake` between 0-255
*  float: `clutch` between 0-1. This seems to correlate with the clutch peddle
*  float: `clutch_engagement` between 0-1
*  float: `clutch_gearbox_rpm`
*  Optional(int): `current_gear` 0-4: current gear, 0 is reverse, None is neutral
*  Optional(int): `suggested_gear`. None if there's no suggested gear
*  List(float): `gear_ratios` 1st - Nth gear. 
*  int: `unused_0x93` always 0
*  int: `unused_0xD4` always 0

## References
[Nenkai](https://github.com/Nenkai) is the original discoverer of this API and how to decrypt and communicate with it, as well as a significant amount of research into each value.

[tarnheld](https://www.gtplanet.net/forum/threads/gt7-is-compatible-with-motion-rig.410728/page-4) for their work in identifying data values/ranges. 