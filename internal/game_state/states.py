from __future__ import annotations
from marshmallow_dataclass import dataclass as marshmallow_dataclass
from typing import Union, List, Optional, Tuple
from granturismo.model import Packet
from granturismo.utils.settings import Settings
from enum import Enum
import json


class Operator(Enum):
  EQ = 0
  GT = 1
  LT = 2
  OR = 3
  XOR = 4
  AND = 5


@marshmallow_dataclass(frozen=True)
class Comparable(object):
    operator: Operator
    value: Union[None, int, float, bool, Tuple[Comparable, Comparable]]


@marshmallow_dataclass
class State:
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

  def __eq__(self, other):
    if self.lap_count is not None and isinstance(self.lap_count.value, str):
      lap_count_other = other.laps_in_race
    else:
      lap_count_other = other.lap_count

    if isinstance(other, self.__class__):
      return self._compare(self.best_lap_time, other.best_lap_time) \
             and self._compare(self.last_lap_time, other.last_lap_time) \
             and self._compare(self.lap_count, lap_count_other) \
             and self._compare(self.laps_in_race, other.laps_in_race) \
             and self._compare(self.cars_in_race, other.cars_in_race) \
             and self._compare(self.start_position, other.start_position) \
             and self._compare(self.car_on_track, other.car_on_track) \
             and self._compare(self.loading_or_processing,  other.loading_or_processing) \
             and self._compare(self.paused, other.paused)
    elif isinstance(other, Packet):
      return self._compare(self.best_lap_time, other.best_lap_time) \
             and self._compare(self.last_lap_time, other.last_lap_time) \
             and self._compare(self.lap_count, lap_count_other) \
             and self._compare(self.laps_in_race,  other.laps_in_race) \
             and self._compare(self.cars_in_race,  other.cars_in_race) \
             and self._compare(self.start_position, other.start_position) \
             and self._compare(self.car_on_track, other.flags.car_on_track) \
             and self._compare(self.loading_or_processing, other.flags.loading_or_processing) \
             and self._compare(self.paused, other.flags.paused)
    return False

  def __str__(self):
    return f'State(name:         : {self.name}\n' + \
           f'      best_lap_time : {self._cstr(self.best_lap_time)}\n' + \
           f'      last_lap_time : {self._cstr(self.last_lap_time)}\n' + \
           f'      lap_count     : {self._cstr(self.lap_count)}\n' + \
           f'      laps_in_race  : {self._cstr(self.laps_in_race)}\n' + \
           f'      cars_in_race  : {self._cstr(self.cars_in_race)}\n' + \
           f'      start_position: {self._cstr(self.start_position)}\n' + \
           f'      car_on_track  : {self._cstr(self.car_on_track)}\n' + \
           f'      paused        : {self._cstr(self.paused)}\n' + \
           f'      loading       : {self._cstr(self.loading_or_processing)}'

  def __repr__(self):
    return self.__str__()

  def add_edge(self, state: State) -> None:
    self._edges.append(state)

  @staticmethod
  def _cstr(c: Optional[Comparable]) -> str:
    if c is None:
      return 'None'
    if c.operator == Operator.EQ:
      return f'== {c.value}'
    elif c.operator == Operator.LT:
      return f' < {c.value}'
    elif c.operator == Operator.GT:
      return f' > {c.value}'

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

    try:
      lhs_op, lhs_val = comparable.value[0].operator, comparable.value[0].value
      rhs_op, rhs_val = comparable.value[1].operator, comparable.value[1].value
      lhs = State._compare(lhs_op, lhs_val)
      rhs = State._compare(rhs_op, rhs_val)
    except Exception as e:
      return

    if comparable.operator == Operator.OR:
      return lhs or rhs
    if comparable.operator == Operator.XOR:
      return (lhs or rhs) and not (lhs and rhs)
    if comparable.operator == Operator.AND:
      return lhs and rhs


class States(object):
  def __init__(self):
    root_dir = Settings().project_directory()
    self._state_file = root_dir.joinpath('data', 'states', 'states.json')
    with open(self._state_file) as f:
      state_dict = json.load(f)

    self._states = {}
    for name, values in state_dict.items():
      self._states[name] = self._build_state(values['packet'], name)

  def _build_state(self, values: dict, name) -> State:
    kwargs = {
      "best_lap_time": None,
      "cars_in_race": None,
      "loading_or_processing": None,
      "car_on_track": None,
      "paused": None,
      "lap_count": None,
      "laps_in_race": None,
      "last_lap_time": None,
      "start_position": None
    }
    kwargs.update(dict(map(lambda tpl: (tpl[0], self._dict_to_comparable(tpl[1])),
                           filter(lambda tpl: tpl[0] in kwargs, values.items()))))
    kwargs['name'] = name
    kwargs['edges'] = []
    return State(**kwargs)

  def get_matching_states(self, p: Packet) -> [State]:
    matches = list(filter(lambda s: s == p, self._states.values()))
    if len(matches) > 0:
      return matches[0]

    kwargs = Packet.Schema().dump(p)
    kwargs['loading_or_processing'] = kwargs['flags']['loading_or_processing']
    kwargs['paused'] = kwargs['flags']['paused']
    kwargs['car_on_track'] = kwargs['flags']['car_on_track']
    return self._build_state(kwargs, 'UNKNOWN')

  @staticmethod
  def _dict_to_comparable(d: Union[dict, None, int, float]) -> Optional[Comparable]:
    if d is None:
      return None

    # this is for when we're loading a packet into a state
    if isinstance(d, int) or isinstance(d, float):
      return Comparable(Operator.EQ, d)

    op = Operator[d['op'].upper()]
    value = d["value"]
    if isinstance(value, list):
      value = States._dict_to_comparable(value[0]), States._dict_to_comparable(value[1])
    else:
      value = d['value']

    return Comparable(op, value)