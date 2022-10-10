from granturismo.utils.settings import Settings
import matplotlib.pyplot as plt
import json
from pathlib import Path

settings = Settings()
input_dir = Path(settings.project_directory().joinpath('data', 's-10'))


def load(filepath: Path):
  with open(filepath) as f:
    content = json.load(f)
    x = []
    y = []
    c = []
    i = 10
    _max_c = 0
    while i < len(content) - 100:
      item = content[i]
      i += 1
      x.append(item['pos'][0])
      y.append(item['pos'][1])
      c.append(item['speed'])
      _max_c = max(item['speed'], _max_c)
    c = list(map(lambda _c: _c / _max_c, c))
    return {'x': x, 'y': y, 'c': c}


if __name__ == '__main__':
  fig, ax = plt.subplots(figsize=(8, 8))
  ax.axis('off')

  filepaths = list(input_dir.glob('*.json'))
  for filepath in filepaths:
    data = load(filepath)
    plt.scatter(data['x'], data['y'], c=data['c'], cmap='plasma', alpha=0.01, s=1)

  plt.gca().set_aspect('equal', adjustable='box')
  plt.title('140 S-10 License attempts')
  plt.xticks([])
  plt.yticks([])
  plt.tight_layout()
  plt.show()