from __future__ import annotations
from typing import List, Optional
from marshmallow_dataclass import dataclass as marshmallow_dataclass
import struct
import math
from granturismo.utils import ntoh
from granturismo.model.common import (
  Vector,
  Rotation,
  Wheel,
  Wheels,
  Bounds,
  Flags
)


@marshmallow_dataclass(frozen=True)
class Packet:
  packet_id: int
  received_time: float
  car_id: int
  lap_count: Optional[int]
  laps_in_race: Optional[int]
  best_lap_time: Optional[int]
  last_lap_time: Optional[int]

  position: Vector
  velocity: Vector
  angular_velocity: Vector
  rotation: Rotation

  road_plane: Vector
  road_distance: float # should match body_height when car is on ground

  wheels: Wheels
  flags: Flags

  orientation: float
  body_height: float
  engine_rpm: float
  gas_level: float
  gas_capacity: float
  car_speed: float
  turbo_boost: float
  oil_pressure: float
  oil_temperature: float
  water_temperature: float
  time_of_day: int
  start_position: Optional[int]
  cars_in_race: Optional[int]
  rpm_alert: Bounds
  car_max_speed: float or int # this is a 2-byte value, so cannot convert to float natively
  transmission_max_speed: float
  throttle: float
  brake: float
  clutch: float
  clutch_engagement: float
  clutch_gearbox_rpm: float
  current_gear: int
  suggested_gear: Optional[int]
  gear_ratios: List[float]

  unused_0x93: int
  unused_0xD4: int # location 212 or 0xD4 in hex

  @staticmethod
  def from_bytes(b: bytearray, received_time: float) -> Packet:
    """
    Constructor for Packet object.
    This will unpack the buffer and return a new instance of Packet
    :param b: The decrypted buffer from PlayStation
    :param received_time: The time the packet was received, before any decoding or deciphering
    :return: new instance of Packet class
    """
    token = b[:4][::-1].decode('ascii')
    if token != 'G7S0':
      raise ValueError(f'Token is invalid! Got {token} but expected G7S0')

    last_lap_time = Packet._get_int(b, 124)
    if last_lap_time == 4294967295:
      last_lap_time = None

    best_lap_time = Packet._get_int(b, 120)
    if best_lap_time == 4294967295:
      best_lap_time = None

    start_position = Packet._get_int(b, 132) >> 4
    # usually the start position is 268435455 (b'11111111 11111111 11111111 11111111')
    # but sometimes it's 4096 (b'00000000 00000000 00001111 11111111')
    if start_position >= 4096:
      start_position = None

    cars_in_race = Packet._get_int(b, 132) & 255
    if cars_in_race == 255:
      cars_in_race = None

    suggested_gear = Packet._get_int(b, 144, 1) >> 4
    if suggested_gear == 15:
      suggested_gear = None

    current_gear = Packet._get_int(b, 144, 1) & 15
    if current_gear == 15:
      current_gear = None


    lap_count = Packet._get_int(b, 116, 2)
    if lap_count == 65535:
      lap_count = None
    laps_in_race = Packet._get_int(b, 118, 2)
    if laps_in_race == 65535:
      laps_in_race = None

    return Packet(
      packet_id=Packet._get_int(b, 112),
      received_time=received_time,
      car_id=Packet._get_int(b, 292),
      lap_count=lap_count,
      laps_in_race=laps_in_race,
      best_lap_time=best_lap_time,
      last_lap_time=last_lap_time,
      position=Vector(
        x=Packet._get_float(b, 4),
        y=Packet._get_float(b, 8),
        z=Packet._get_float(b, 12)
      ),
      velocity=Vector(
        x=Packet._get_float(b, 16),
        y=Packet._get_float(b, 20),
        z=Packet._get_float(b, 24)
      ),
      angular_velocity=Vector(
        x=Packet._get_float(b, 44),
        y=Packet._get_float(b, 48),
        z=Packet._get_float(b, 52)
      ),
      rotation=Rotation(
        pitch=Packet._get_float(b, 28),
        yaw=Packet._get_float(b, 32),
        roll=Packet._get_float(b, 36)
      ),
      road_plane=Vector(
        x=Packet._get_float(b, 148),
        y=Packet._get_float(b, 152),
        z=Packet._get_float(b, 156)
      ),
      road_distance=Packet._get_float(b, 160),
      wheels=Wheels(
        front_left=Wheel(
          suspension_height=Packet._get_float(b, 196),
          radius=Packet._get_float(b, 180),
          rps=math.degrees(Packet._get_float(b, 164)) / 360.,
          ground_speed=2 * math.pi * Packet._get_float(b, 180) * math.degrees(Packet._get_float(b, 164)) / 360.,
          temperature=Packet._get_float(b, 96)),
        front_right=Wheel(
          suspension_height=Packet._get_float(b, 200),
          radius=Packet._get_float(b, 184),
          rps=math.degrees(Packet._get_float(b, 168)) / 360.,
          ground_speed=2 * math.pi * Packet._get_float(b, 184) * math.degrees(Packet._get_float(b, 168)) / 360.,
          temperature=Packet._get_float(b, 100)),
        rear_left=Wheel(
          suspension_height=Packet._get_float(b, 204),
          radius=Packet._get_float(b, 188),
          rps=math.degrees(Packet._get_float(b, 172)) / 360.,
          ground_speed=2 * math.pi * Packet._get_float(b, 188) * math.degrees(Packet._get_float(b, 172)) / 360.,
          temperature=Packet._get_float(b, 104)),
        rear_right=Wheel(
          suspension_height=Packet._get_float(b, 208),
          radius=Packet._get_float(b, 192),
          rps=math.degrees(Packet._get_float(b, 176)) / 360.,
          ground_speed=2 * math.pi * Packet._get_float(b, 193) * math.degrees(Packet._get_float(b, 176)) / 360.,
          temperature=Packet._get_float(b, 108)),
      ),
      flags=Packet._get_flags(b, 142),
      orientation=Packet._get_float(b, 40),
      body_height=Packet._get_float(b, 56),
      engine_rpm=Packet._get_float(b, 60),
      gas_level=Packet._get_float(b, 68),
      gas_capacity=Packet._get_float(b, 72),
      car_speed=Packet._get_float(b, 76),
      turbo_boost=Packet._get_float(b, 80),
      oil_pressure=Packet._get_float(b, 84),
      water_temperature=Packet._get_float(b, 88),
      oil_temperature=Packet._get_float(b, 92),
      time_of_day=Packet._get_int(b, 128),
      start_position=start_position,
      cars_in_race=cars_in_race,
      rpm_alert=Bounds(
        min=Packet._get_int(b, 136, 2),
        max=Packet._get_int(b, 138, 2)
      ),
      car_max_speed=Packet._get_int(b, 140, 2),
      transmission_max_speed=Packet._get_float(b, 256),
      throttle=Packet._get_int(b, 145, 1),
      brake=Packet._get_int(b, 146, 1),
      clutch=Packet._get_float(b, 244),
      clutch_engagement=Packet._get_float(b, 248),
      clutch_gearbox_rpm=Packet._get_float(b, 252),
      current_gear=current_gear,
      suggested_gear=suggested_gear,
      gear_ratios=Packet._get_gear_ratios(b, 260),
      unused_0x93 = Packet._get_int(b, 147, 1),
      unused_0xD4 = Packet._get_int(b, 212, 32)
    )

  @staticmethod
  def _get_float(b: bytearray, i: int, size: int=4) -> float:
    return struct.unpack('f', ntoh(b[i:i+size]))[0]

  @staticmethod
  def _get_int(b: bytearray, i: int, size: int=4) -> int:
    return int.from_bytes(ntoh(b[i:i+size]), 'little')

  @staticmethod
  def _get_flags(b: bytearray, i: int) -> Flags:
    m = 1
    a = Packet._get_int(b, i, 2)
    return Flags(
      car_on_track=bool(a & m),
      paused=bool(a & (m << 1)),
      loading_or_processing=bool(a & (m << 2)),
      in_gear=bool(a & (m << 3)),
      has_turbo=bool(a & (m << 4)),
      rev_limiter_alert_active=bool(a & (m << 5)),
      hand_brake_active=bool(a & (m << 6)),
      lights_active=bool(a & (m << 7)),
      lights_high_beams_active=bool(a & (m << 8)),
      lights_low_beams_active=bool(a & (m << 9)),
      asm_active=bool(a & (m << 10)),
      tcs_active=bool(a & (m << 11)),
      unused1=bool(a & (m << 12)),
      unused2=bool(a & (m << 13)),
      unused3=bool(a & (m << 14)),
      unused4=bool(a & (m << 15))
    )

  @staticmethod
  def _get_gear_ratios(b: bytearray, i: int) -> List[float]:
    ratios = []
    for gear_number in range(8):
      ratio = Packet._get_float(b, i + (gear_number * 4))
      if ratio == 0:
        break
      ratios.append(ratio)
    return ratios


