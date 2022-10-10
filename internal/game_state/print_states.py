from granturismo.intake import Listener
from granturismo.model import Packet
from internal.game_state.states import States
import datetime as dt
import json


def state_to_dict(p: Packet) -> dict:
  return {
    'best_lap_time': str(dt.timedelta(seconds=p.best_lap_time / 1000)) if p.best_lap_time is not None else None,
    'last_lap_time': str(dt.timedelta(seconds=p.last_lap_time / 1000)) if p.last_lap_time is not None else None,
    'cars_in_race': p.cars_in_race,
    'start_position': p.start_position,
    'lap_count': p.lap_count,
    'laps_in_race': p.laps_in_race,
    'car_on_track': p.flags.car_on_track,
    'loading_or_processing': p.flags.loading_or_processing,
    'paused': p.flags.paused,
    'gas_capacity': p.gas_capacity
  }


if __name__ == '__main__':
  states = States()
  prev_state = None

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
        print(f'state:[{name}]')
        if name == 'UNKNOWN':
          print(json.dumps(state_to_dict(packet), indent=4))
