from granturismo.model.common import *
from granturismo.model import Packet


def vector2dict(v: Vector) -> dict:
  return {
    'x': v.x,
    'y': v.y,
    'z': v.z
  }


def dict2vector(d: dict) -> Vector:
  return Vector(**d)


def wheel2dict(w: Wheel) -> dict:
  return {
    'suspension_height': w.suspension_height,
    'radius': w.radius,
    'rps': w.rps,
    'ground_speed': w.ground_speed,
    'temperature': w.temperature
  }


def dict2wheel(d: dict) -> Wheel:
  return Wheel(**d)


def flags2dict(f: Flags) -> dict:
  return {
    'car_on_track': f.car_on_track,
    'paused': f.paused,
    'loading_or_processing': f.loading_or_processing,
    'in_gear': f.in_gear,
    'has_turbo': f.has_turbo,
    'rev_limiter_alert_active': f.rev_limiter_alert_active,
    'hand_brake_active': f.hand_brake_active,
    'lights_active': f.lights_active,
    'lights_high_beams_active': f.lights_high_beams_active,
    'lights_low_beams_active': f.lights_low_beams_active,
    'asm_active': f.asm_active,
    'tcs_active': f.tcs_active,
    'unused1': f.unused1,
    'unused2': f.unused2,
    'unused3': f.unused3,
    'unused4': f.unused4
  }


def dict2flags(d: dict) -> Flags:
  return Flags(**d)


def packet2dict(p: Packet) -> dict:
  return {
    'packet_id': p.packet_id,
    'retrieved_time': p.received_time,
    'car_id': p.car_id,
    'lap_count': p.lap_count,
    'laps_in_race': p.laps_in_race,
    'best_lap_time': p.best_lap_time,
    'last_lap_time': p.last_lap_time,
    'position': vector2dict(p.position),
    'velocity': vector2dict(p.velocity),
    'angular_velocity': vector2dict(p.angular_velocity),
    'rotation': {
      'pitch': p.rotation.pitch,
      'yaw': p.rotation.yaw,
      'roll': p.rotation.roll
    },
    'road_plane': vector2dict(p.road_plane),
    'road_distance': p.road_distance,
    'wheels': {
      'front_left': wheel2dict(p.wheels.front_left),
      'front_right': wheel2dict(p.wheels.front_right),
      'rear_left': wheel2dict(p.wheels.rear_left),
      'rear_right': wheel2dict(p.wheels.rear_right)
    },
    'flags': flags2dict(p.flags),
    'orientation': p.orientation,
    'body_height': p.body_height,
    'engine_rpm': p.engine_rpm,
    'gas_level': p.gas_level,
    'gas_capacity': p.gas_capacity,
    'car_speed': p.car_speed,
    'turbo_boost': p.turbo_boost,
    'oil_pressure': p.oil_pressure,
    'oil_temperature': p.oil_temperature,
    'water_temperature': p.water_temperature,
    'time_of_day': p.time_of_day,
    'start_position': p.start_position,
    'cars_in_race': p.cars_in_race,
    'rpm_alert': {
      'min': p.rpm_alert.min,
      'max': p.rpm_alert.max
    },
    'car_max_speed': p.car_max_speed,
    'transmission_max_speed': p.transmission_max_speed,
    'throttle': p.throttle,
    'brake': p.brake,
    'clutch': p.clutch,
    'clutch_engagement': p.clutch_engagement,
    'clutch_gearbox_rpm': p.clutch_gearbox_rpm,
    'current_gear': p.current_gear,
    'suggested_gear': p.suggested_gear,
    'gear_ratios': p.gear_ratios,
    'unused_0x93': p.unused_0x93,
    'unused_0xD4': p.unused_0xD4
  }


def dict2packet(d: dict) -> Packet:
  d['position'] = dict2vector(d['position'])
  d['velocity'] = dict2vector(d['velocity'])
  d['angular_velocity'] = dict2vector(d['angular_velocity'])
  d['road_plane'] = dict2vector(d['road_plane'])
  d['rotation'] = Rotation(
    pitch=d['rotation']['pitch'],
    yaw=d['rotation']['yaw'],
    roll=d['rotation']['roll'])
  d['rpm_alert'] = Bounds(
    min=d['rpm_alert']['min'],
    max=d['rpm_alert']['max'])
  d['wheels'] = Wheels(
    front_left=dict2wheel(d['wheels']['front_left']),
    front_right=dict2wheel(d['wheels']['front_right']),
    rear_left=dict2wheel(d['wheels']['rear_left']),
    rear_right=dict2wheel(d['wheels']['rear_right']))
  d['flags'] = dict2flags(d['flags'])

  return Packet(**d)
