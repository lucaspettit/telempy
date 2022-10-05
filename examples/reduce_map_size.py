import math, json
from typing import Tuple
from pathlib import Path


def sub2(tpl: Tuple[float, float]) -> float:
  return math.pow(tpl[0] - tpl[1], 2)


def distance(a: Tuple[float, float, float], b: Tuple[float, float, float]) -> float:
  return math.sqrt(sum(map(sub2, zip(a, b))))


if __name__ == '__main__':
  src = Path('/data/trackDataRaw')
  dest = Path('/data/trackData')

  srcfiles = list(src.glob('*.json'))
  for filename in srcfiles:
    track_name = filename.name.rsplit('.', 1)[0]
    print(f'[{track_name}]')
    with open(filename) as f:
      track = json.load(f)

    positions = [(p['position']['x'], p['position']['y'], p['position']['z']) for p in track['packets']]
    _positions = [positions[0]]

    a = _positions[-1]
    for i in range(1, len(positions)):
      b = positions[i]
      dist = distance(a, b)
      if dist >= 10:
        a = b
        _positions.append(b)

    print(f'  Reduced from [{len(positions)}] to [{len(_positions)}]')
    del track['packets']
    track['coords'] = _positions
    with open(dest.joinpath(filename.name), 'w') as f:
      json.dump(track, f)





