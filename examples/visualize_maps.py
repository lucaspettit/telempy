import matplotlib.pyplot as plt
from pathlib import Path
import json

if __name__ == '__main__':
  track_files = list(Path('/data/trackData').glob('*.json'))


  for filename in track_files:
    with open(filename) as f:
      track = json.load(f)
    x = [p['position']['x'] for p in track['packets']]
    z = [-p['position']['z'] for p in track['packets']]
    plt.scatter(x, z, label=track['track']['name'], s=1)

  plt.legend()
  plt.scatter([0], [0], marker='+', color='r', zorder=2)
  plt.tight_layout()
  plt.show()
