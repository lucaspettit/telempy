from granturismo.intake import Listener
from granturismo.model.common import Vector
from granturismo.utils.settings import Settings
from internal.game_state.states import States, State
import json


settings = Settings()
prev_state: State = None


def save_packets(car_id, packets):
  track_name = input('track name     : ')
  layout =     input('layout   [null]: ')
  car_name =   input('car name [null]: ')
  event =      input('event    [null]: ') # <license name> or <ce-{id}>

  filename = track_name + (f' - {layout}' if layout else '') + '.json'
  filename = output_dir.joinpath(filename)
  content = {
    'track': {
      'id': len(list(output_dir.glob('*.json'))),
      'name': track_name,
      'layout': layout if layout else None,
      'event': event
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


def get_state(packet):
  global prev_state
  state = states.get_matching_states(packet)

  _prev_state = prev_state
  if prev_state is None or prev_state.name != state.name:
    prev_state = state
  if state.name == 'UNKNOWN' and prev_state != state:
    schema = State.Schema().dump(state)
    keys = [
      'best_lap_time',
      'last_lap_time',
      'lap_count',
      'laps_in_race',
      'cars_in_race',
      'start_position',
      'car_on_track',
      'loading_or_processing',
      'paused'
    ]
    for k in keys:
      v = schema[k]
      if not v is None:
        if k in {'loading_or_processing', 'car_on_track', 'paused'}:
          v = v['value'] == 1
        else:
          v = v['value']
      print(f'  {k}: {v}')
    print('-' * 50)
  return state


if __name__ == '__main__':
  from pathlib import Path
  import sys

  states = States()
  prev_state = None
  racing = {'BEFORE_RACE_START', 'RACING', 'AFTER_RACE_END', 'PAUSED', 'LOADING', 'DEMONSTRATION', 'BEFORE_TIME_TRIAL_START', 'TIME_TRIAL_RACING'}
  racing_capture_mode = {'BEFORE_RACE_START', 'RACING', 'AFTER_RACE_END', 'DEMONSTRATION', 'BEFORE_TIME_TRIAL_START', 'TIME_TRIAL_RACING'}

  output_dir = Path(settings.project_directory().joinpath('data', 'trackDataRaw'))
  output_dir.mkdir(parents=True, exist_ok=True)
  track_id = len(list(output_dir.glob('*.json')))
  packets = []
  car_id = None

  previous_state = ''
  previous_packet = None
  capture = False
  capture_count = 0

  with Listener(sys.argv[1]) as listener:
    while True:
      packet = listener.get()
      state = get_state(packet)

      if not previous_state:
        previous_state = state.name
      elif previous_state != state.name:
        print(f'{state.name} {capture_count}')
        capture_count = 0
        previous_state = state.name
      capture_count += 1

      if not capture and state.name in {'BEFORE_RACE_START', 'BEFORE_TIME_TRIAL_START'}:
        capture = True
        print('  Capture started')

      elif capture and state.name not in racing:
        capture = False
        print('  Capture ended')
        save_packets(car_id, packets)
        packets = []
        car_id = None

      elif capture and state.name in racing_capture_mode:
          if car_id is None:
            car_id = packet.car_id
          packets.append({
            'position': Vector.Schema().dump(packet.position),
            'speed': packet.car_speed,
            'brake': packet.brake,
            'throttle': packet.throttle,
            'clutch': packet.clutch,
            'currentGear': packet.current_gear
          })

      previous_packet = packet