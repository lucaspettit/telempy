from granturismo.intake import Listener
from granturismo.model import Packet
from granturismo.utils.settings import Settings
from internal.game_state.states import States
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

  output_dir = Path(settings.project_directory().joinpath('data', 's-10'))
  output_dir.mkdir(parents=True, exist_ok=True)

  attempt = len(list(output_dir.glob('*.json')))
  content = []
  capture = False

  with Listener('192.168.1.207') as listener:
    while True:
      packet = listener.get()
      matches = states.get_matching_states(packet)
      if len(matches) > 0:
        name = matches[0].name
      else:
        name = 'UNKNOWN'

      if prev_state != name:
        prev_state = name

      if not capture and name == 'RACING':
        capture = True
        print('Capture started')
      elif capture and name not in racing:
          capture = False
          print('Capture ended')
          with open(output_dir.joinpath(f'{attempt}.json'), 'w') as f:
            json.dump(content, f)
          attempt += 1
          content = []
      elif capture and name == 'RACING':
          content.append({
            'pos': (packet.position.x, -packet.position.z),
            'speed': packet.car_speed
          })
