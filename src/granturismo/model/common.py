from marshmallow_dataclass import dataclass as marshmallow_dataclass
from marshmallow import validate
from dataclasses import field
import enum


class CarType(enum.Enum):
  UNKNOWN=0
  GAS=1
  ELECTRIC=2
  KART=3


class GameState(enum.Enum):
  UNKNOWN=0
  MENU=1
  PRE_RACE=2
  RACE=3
  POST_RACE=4
  TIME_TRIAL=5
  CIRCUIT_EXP_SECTOR=6


@marshmallow_dataclass(frozen=True)
class Vector:
  x: float
  y: float
  z: float


@marshmallow_dataclass(frozen=True)
class Rotation:
  pitch: float
  yaw: float
  roll: float


@marshmallow_dataclass(frozen=True)
class Wheel:
  suspension_height: float = field(metadata={'validate': validate.Range(min=0, max=1)})
  radius: float # in meters
  rps: float # rotations per second (not radians like default)
  ground_speed: float # meters per second
  temperature: float


@marshmallow_dataclass(frozen=True)
class Wheels:
  front_left: Wheel
  front_right: Wheel
  rear_left: Wheel
  rear_right: Wheel


@marshmallow_dataclass(frozen=True)
class Bounds:
  min: float
  max: float


@marshmallow_dataclass(frozen=True)
class Flags:
  car_on_track: bool
  paused: bool
  loading_or_processing: bool
  in_gear: bool
  has_turbo: bool
  rev_limiter_alert_active: bool
  hand_brake_active: bool
  lights_active: bool
  lights_high_beams_active: bool
  lights_low_beams_active: bool
  asm_active: bool
  tcs_active: bool
  unused1: bool
  unused2: bool
  unused3: bool
  unused4: bool
