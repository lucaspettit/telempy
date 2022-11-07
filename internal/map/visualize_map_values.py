import json
import matplotlib.pyplot as plt
from matplotlib import gridspec
from granturismo.utils.settings import Settings


def plot_hist(ax, values, label=None):
  heights, _, _ = ax.hist(values, bins=50, facecolor='r', alpha=0.5, density=True)
  height = max(heights)
  median = sorted(values)[int(len(values) / 2)]
  ax.plot([median, median], [0, height], linewidth=1, color='k')
  if label:
    ax.set_xlabel(label)

def plot(xs, ys, zs):
  fig = plt.figure(figsize=(12, 8))
  top_left = plt.subplot2grid(shape=(3, 3), loc=(0, 0))
  middle_left = plt.subplot2grid(shape=(3, 3), loc=(1, 0))
  bottom_left = plt.subplot2grid(shape=(3, 3), loc=(2, 0))
  right = plt.subplot2grid(shape=(3, 3), loc=(0, 1), colspan=2, rowspan=3)
  for ax in (top_left, middle_left, bottom_left, right):
    ax.set_xticks([])
    ax.set_yticks([])

  for _xs, _zs in zip(xs, zs):
    right.plot(_xs, _zs, linewidth=1)
  right.scatter([0], [0], s=50, c='r', marker='+')

  x, y, z = [], [], []
  for _x, _y, _z in zip(xs, ys, zs):
    x.extend(_x)
    y.extend(_y)
    z.extend(_z)

  plot_hist(top_left, x, 'X')
  plot_hist(middle_left, y, 'Y')
  plot_hist(bottom_left, z, 'Z')
  plt.tight_layout()
  plt.show()


if __name__ == '__main__':
  package_dir = Settings().project_directory()
  map_files = list(package_dir.joinpath('data', 'trackData').glob('*.json'))

  print(f'Found {len(map_files)} tracks')
  xs, ys, zs = [], [], []
  for filename in map_files:
    with open(filename) as f:
      data = json.load(f)
      if data['track']['name'] == 'Special Stage Route X':
        continue

      x, y, z = [], [], []
      for (_x, _y, _z) in data['coords']:
        x.append(_x)
        y.append(_y)
        z.append(_z)
      xs.append(x)
      ys.append(y)
      zs.append(z)

  plot(xs, ys, zs)