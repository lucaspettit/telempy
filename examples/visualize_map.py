import matplotlib.pyplot as plt
import json
import time

if __name__ == '__main__':
  with open('position_coords.json') as f:
    pos = json.load(f)

  x =  pos['x']#list(map(lambda x: -x, pos['x']))
  z = list(map(lambda z: -z, pos['z']))

  x_min = min(x)
  x_max = max(x)
  x_min = x_min - (0.05 * (x_max - x_min))
  x_max = x_max + (0.05 * (x_max - x_min))

  z_min = min(z)
  z_max = max(z)
  z_min = z_min - (0.05 * (z_max - z_min))
  z_max = z_max + (0.05 * (z_max - z_min))

  print(x_min, x_max)
  print(z_min, z_max)

  plt.ion()
  fig = plt.figure(figsize=(10, 10))
  for i in range(1, len(x), 1):
    plt.scatter(x[i], z[i], s=1, c='b')
    plt.ylim(z_min, z_max)
    plt.xlim(x_min, x_max)
    plt.draw()
    plt.pause(0.000001)
    #plt.clf()

  # fig = plt.figure(figsize=(10, 10))
  # plt.scatter(x, z, s=1)
  # plt.ylim(z_min, z_max)
  # plt.xlim(x_min, x_max)
  # plt.show()
