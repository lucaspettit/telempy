from granturismo.intake import Listener
from granturismo.model import Packet
from granturismo.utils.settings import Settings
from typing import Dict
from pprint import pprint
from states.state import States
import datetime as dt
import json


tracked_vars: dict = None
packet_count: int = 0
settings = Settings()


def build_tracked_vars(p: Packet) -> dict:
  return {
    'best_lap_time': str(dt.timedelta(seconds=p.best_lap_time / 1000)) if p.best_lap_time is not None else None,
    'last_lap_time': str(dt.timedelta(seconds=p.last_lap_time / 1000)) if p.last_lap_time is not None else None,
    'cars_in_race': p.cars_in_race,
    'start_position': p.start_position,
    'lap_count': p.lap_count,
    'laps_in_race': p.laps_in_race,
    'loading_or_processing': p.flags.loading_or_processing,
    'gas_capacity': p.gas_capacity
  }

def compare(a: dict, b: dict) -> Dict[str, str]:
  output = {}
  for k, v in a.items():
    if isinstance(v, dict):
      res = compare(v, b[k])
      for _k, _v in res.items():
        output[f'{k}.{_k}'] = _v
    else:
      if v != b[k]:
        output[k] = f'{b[k]} -> {v}'
  return output


def get_state(packet: Packet) -> str:
  global tracked_vars, packet_count
  new_vars = build_tracked_vars(packet)
  if tracked_vars is None:
    packet_count += 1
    tracked_vars = new_vars
    pprint(tracked_vars)
  else:
    diff = compare(new_vars, tracked_vars)
    if len(diff) > 0:

      tracked_vars = new_vars
      print('-' * 100)
      print(f'COUNT={packet_count}')
      pprint(diff)
      packet_count = 0
    else:
      packet_count += 1
  # unused = packet.unused_0x93.to_bytes(4, 'little')
  # unused = struct.unpack('f', unused)
  # print(f'unused_0x93={unused}')


if __name__ == '__main__':
  from pathlib import Path
  states = States()
  prev_state = None
  non_menu = {
    'RACE_MENU',
    'BEFORE_RACE_START',
    'RACING',
    'AFTER_RACE_END'
    }
  racing = {'RACING', 'PAUSED'}

  output_dir = Path(settings.project_directory().joinpath('data', 'trackDataRaw'))
  output_dir.mkdir(parents=True, exist_ok=True)
  attempt = len(list(output_dir.glob('*.json')))
  packets = []
  car_id = None
  capture = False

  with Listener('192.168.1.207') as listener:
    while True:
      #get_state(listener.get())

      packet = listener.get()
      if packet.flags.paused:
        name = 'PAUSED'
      elif packet.flags.loading_or_processing:
        name = 'LOADING'
      else:
        matches = states.get_matching_states(packet)
        if len(matches) > 0:
          name = [m.name for m in matches][0]
          if name not in non_menu:
            name = 'MENU'
        else:
          name = 'N/A'

      if prev_state != name:
        prev_state = name
        print(name)
        #if name == 'N/A':
        #  print(json.dumps(build_tracked_vars(packet), indent=4))

      if not capture and name == 'RACING':
        capture = True
        print('Capture started')
      elif capture and name not in racing:
          capture = False
          print('Capture ended')

          track_name = input('track name? ')
          layout = input('layout? ')
          car_name = input('car name? ')

          filename = track_name + (f' - {layout}' if layout else '') + '.json'
          filename = output_dir.joinpath(filename)
          content = {
            'track': {
              'id': len(list(output_dir.glob('*.json'))),
              'name': track_name,
              'layout': layout if layout else None
            },
            'car': {
              'id': car_id,
              'name': car_name
            },
            'packets': packets
          }

          print(f'Saving to [{filename.name}]')
          with open(output_dir.joinpath(filename), 'w') as f:
            json.dump(content, f)
          packets = []
          car_id = None
          car_name = None
      elif capture and name == 'RACING':
          if car_id is None:
            car_id = packet.car_id
          packets.append({
            'position': packet.position,
            'speed': packet.car_speed,
            'brake': packet.brake,
            'throttle': packet.throttle,
            'clutch': packet.clutch,
            'currentGear': packet.current_gear
          })
