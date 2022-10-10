from __future__ import annotations
from marshmallow_dataclass import dataclass as marshmallow_dataclass
from typing import Union, List, Optional
from granturismo.model import Packet
from enum import Enum
import json


class Operator(Enum):
  EQ = 0
  GT = 1
  LT = 2


@marshmallow_dataclass(frozen=True)
class Comparable(object):
    operator: Operator
    value: Union[None, int, float]


@marshmallow_dataclass
class State(object):
  """
  All states must have a name.
  For all the other values, we will either have a comparable or None if
  we don't care what those values are (ex. PAUSED state - will be paused whenever paused flag is true regardless of other values)
  """
  name: str
  best_lap_time: Optional[Comparable]
  last_lap_time: Optional[Comparable]
  lap_count: Optional[Comparable]
  laps_in_race: Optional[Comparable]
  cars_in_race: Optional[Comparable]
  start_position: Optional[Comparable]

  car_on_track: Optional[Comparable]
  loading_or_processing: Optional[Comparable]
  paused: Optional[Comparable]

  edges: List[State]

  def add_edge(self, state: State) -> None:
    self._edges.append(state)

  @staticmethod
  def _compare(comparable: Optional[Comparable], value: Union[None, int, float]) -> bool:
    if comparable is None:
      return True

    if comparable.operator == Operator.EQ:
      if comparable.value is None:
        return value is None
      return value is not None and comparable.value == value

    if value is None:
      return False

    if comparable.operator == Operator.GT:
      return value > comparable.value
    if comparable.operator == Operator.LT:
      return value < comparable.value

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self._compare(self.best_lap_time, other.best_lap_time) \
        and self._compare(self.last_lap_time, other.last_lap_time) \
        and self._compare(self.lap_count, other.lap_count) \
        and self._compare(self.laps_in_race, other.laps_in_race) \
        and self._compare(self.cars_in_race, other.cars_in_race) \
        and self._compare(self.start_position, other.start_position) \
        and self._compare(self.car_on_track, other.car_on_track) \
        and self._compare(self.loading_or_processing,  other.loading_or_processing) \
        and self._compare(self.paused, other.paused)
    elif isinstance(other, Packet):
      return self._compare(self.best_lap_time, other.best_lap_time) \
        and self._compare(self.last_lap_time, other.last_lap_time) \
        and self._compare(self.lap_count, other.lap_count) \
        and self._compare(self.laps_in_race,  other.laps_in_race) \
        and self._compare(self.cars_in_race,  other.cars_in_race) \
        and self._compare(self.start_position, other.start_position) \
        and self._compare(self.car_on_track, other.flags.car_on_track) \
        and self._compare(self.loading_or_processing, other.flags.loading_or_processing) \
        and self._compare(self.paused, other.flags.paused)
    return False



class States(object):
  def __init__(self):
    self._state_file = '/Users/lpettit/Desktop/Luke/Code/telempy/data/states/states.json'
    with open(self._state_file) as f:
      state_dict = json.load(f)

    self._states = {}
    for name, values in state_dict.items():
      values = values['packet']
      kwargs = dict(map(lambda tpl: (tpl[0], self._dict_to_comparable(tpl[1])), values.items()))
      kwargs['name'] = name
      kwargs['edges'] = []
      self._states[name] = State(**kwargs)

  def get_matching_states(self, p: Packet) -> [State]:
    return list(filter(lambda s: s == p, self._states.values()))

  @staticmethod
  def _dict_to_comparable(d: Union[dict, None]) -> Optional[Comparable]:
    if d is None:
      return None

    if d['op'] == 'eq':
      op = Operator.EQ
    elif d['op'] == 'lt':
      op = Operator.LT
    elif d['op'] == 'gt':
      op = Operator.GT
    else:
      raise Exception(f'Invalid operator {d["op"]}')

    return Comparable(op, d['value'])