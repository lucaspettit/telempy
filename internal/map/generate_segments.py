"""
We need to break the 3D cartesian space into cuboids with
equal number of points. This will likely be a fairly optimized
approach over cubes of equal height, width, and length.

We will maintain a hierarchy of cuboids (like a tree) so that we can
quickly navigate to the cuboid where a specific point resides.

Once we identify the cuboid where our point lives, we'll have to
get the nearest neighbor for all points in the cuboid and the cuboids
neighbors. This might be more tricky than I'm hoping, because since
each cuboid will differ in dimensions, we will likely have many cases
where a cuboid has more than 8 neighbors.
"""
from __future__ import annotations
import json, math
from collections import defaultdict
from pathlib import Path
from typing import Union, List, Tuple, Set, Dict


class SegmentGenerator(object):
  _CUBE_SIZE=100

  def __init__(self,
               input_dir: Union[Path, str],
               output_dir: Union[Path, str]) -> None:
    if isinstance(input_dir, str):
      input_dir = Path(input_dir)
    if isinstance(output_dir, str):
      output_dir = Path(output_dir)
    if not input_dir.is_dir():
      raise Exception(f'Input directory doesn\'t exist: {input_dir}')
    output_dir.mkdir(parents=True, exist_ok=True)
    self._output_dir = output_dir
    self._input_dir = input_dir
    self._head = None

  def generate(self) -> List[List[List[Set[float, float, float]]]]:

    # we need to load in every <x,y,z> vector and tag a track_id and step count
    # we also need to unpack all track info into a dict
    tracks, coords = self._load_track_data()

    # 1. Divide the entire world up into cubes of size (NxNxN).
    #       1.1 Put these cubes into a 3d array so we can index.
    cubes = self._generate_cubes(coords.keys())

    # 2. Walk through every point and assign it to a cube.
    cubes = self._assign_coords_to_cubes(coords.keys(), cubes)

    # 3. Convert all set to list so we can serialize
    for i in range(len(cubes)):
      for j in range(len(cubes[0])):
        for k in range(len(cubes[0][0])):
          cubes[i][j][k] = list(cubes[i][j][k])

    x_min, _ = self._get_initial_range(list(map(lambda tpl: tpl[0], coords)), buffer=self._CUBE_SIZE * 3)
    y_min, _ = self._get_initial_range(list(map(lambda tpl: tpl[1], coords)), buffer=self._CUBE_SIZE)
    z_min, _ = self._get_initial_range(list(map(lambda tpl: tpl[2], coords)), buffer=self._CUBE_SIZE * 3)
    with open(self._output_dir.joinpath('trackCoordinates.json'), 'w') as f:
      json.dump({
        'min': [x_min, y_min, z_min],
        'size': self._CUBE_SIZE,
        'cubes': cubes
      }, f)

    coords = list(coords.items())
    with open(self._output_dir.joinpath('coordToTrackMap.json'), 'w') as f:
      json.dump(coords, f)

    with open(self._output_dir.joinpath('trackMetadata.json'), 'w') as f:
      json.dump(tracks, f)

  def _generate_cubes(self, coords: List[Tuple[float, float, float]]) -> List[List[List[Set[float, float, float]]]]:
    x_min, x_max = self._get_initial_range(list(map(lambda tpl: tpl[0], coords)), buffer=self._CUBE_SIZE * 3)
    y_min, y_max = self._get_initial_range(list(map(lambda tpl: tpl[1], coords)), buffer=self._CUBE_SIZE)
    z_min, z_max = self._get_initial_range(list(map(lambda tpl: tpl[2], coords)), buffer=self._CUBE_SIZE * 3)

    nx = int((x_max - x_min) / self._CUBE_SIZE)
    ny = int((y_max - y_min) / self._CUBE_SIZE)
    nz = int((z_max - z_min) / self._CUBE_SIZE)
    c = []

    for xi in range(nx):
      c.append([])
      for yi in range(ny):
        c[xi].append([])
        for zi in range(nz):
          c[xi][yi].append(set())

    return c

  def _assign_coords_to_cubes(self, coords: List[Tuple[float, float, float]], cubes: List[List[List[Set[float, float, float]]]]) \
      -> List[List[List[Set[float, float, float]]]]:
    x_min, _ = self._get_initial_range(list(map(lambda tpl: tpl[0], coords)), buffer=self._CUBE_SIZE * 3)
    y_min, _ = self._get_initial_range(list(map(lambda tpl: tpl[1], coords)), buffer=self._CUBE_SIZE)
    z_min, _ = self._get_initial_range(list(map(lambda tpl: tpl[2], coords)), buffer=self._CUBE_SIZE * 3)

    print(f'cubes.shape = {(len(cubes), len(cubes[0]), len(cubes[0][0]))}')
    for x, y, z in coords:
      xi = math.floor((x - x_min) / self._CUBE_SIZE)
      yi = math.floor((y - y_min) / self._CUBE_SIZE)
      zi = math.floor((z - z_min) / self._CUBE_SIZE)
      cubes[xi][yi][zi].add((x, y, z))

    return cubes

  def _get_initial_range(self, values: List[float], buffer: int=0) -> Tuple[float, float]:
    # buffer this so it's exactly divisible by 50
    _min, _max = min(values), max(values)
    _center = _min + ((_max - _min) / 2)
    _range = abs(math.ceil((_min + _center) / self._CUBE_SIZE))
    _min2 = _center - (self._CUBE_SIZE * _range) - buffer
    _max2 = _center + (self._CUBE_SIZE * _range) + buffer

    return _min2, _max2

  def _load_track_data(self) \
      -> Tuple[
        Dict[str, Union[int, str]],
        Dict[Tuple[float, float, float], Dict[str, Union[int, str]]]
      ]:
    # generate a list of all the tracks under input_dir
    track_files = list(self._input_dir.glob('*.json'))

    tracks = {} # int -> {id: int, name: str, layout: Optional[str]}
    coords = defaultdict(list) # (x,y,z) -> [{trackId: int, step: int}, ...]

    for filename in track_files:
      with open(filename) as f:
        data = json.load(f)
      track = data['track']
      track_id = track['id']
      tracks[track_id] = track

      for step, coord in enumerate(data['coords']):
        coord = tuple(coord)
        coords[coord].append({'trackId': track_id, 'step': step})

    return tracks, coords

if __name__ == '__main__':
  generator = SegmentGenerator('/Users/lpettit/Desktop/Luke/Code/telempy/data/trackData', '/Users/lpettit/Desktop/Luke/Code/telempy/data/cuboids')
  generator.generate()

