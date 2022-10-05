import matplotlib.pyplot as plt
import json
import time
import math
from src.utils.debug import to_bit_str

if __name__ == '__main__':
  with open('packets.json') as f:
    packets = json.load(f)

  meters_seconds_to_miles_hours = 2.2369356

  velocities = [p['velocity'] for p in packets if p['lapCount'] == 1]
  velocities = [math.sqrt(math.pow(v['x'], 2) + math.pow(v['y'], 2) + math.pow(v['z'], 2)) * meters_seconds_to_miles_hours for v in velocities]
  car_speed = [p['carSpeed'] * meters_seconds_to_miles_hours for p in packets if p['lapCount'] == 1]
  drift = [True if abs(v - s) > 1 else False for v, s in zip(velocities, car_speed)]
  position = [(p['position']['x'], -p['position']['z']) for p in packets if p['lapCount'] == 1]

  for dist in [p['roadPlaneDistance'] for p in packets]:
    print(to_bit_str(dist))

  not_drifting = [p for p, d in zip(position, drift) if d]
  drifting = [p for p, d in zip(position, drift) if not d]

  x = [x for x, _ in position]
  y = [y for _, y in position]
  fig, ax = plt.subplots(figsize=(10, 10))
  points = ax.scatter(x, y, c=car_speed, cmap='plasma', s=1)
  fig.colorbar(points)
  ax.set_xticks([])
  ax.set_yticks([])
  plt.title('Nurburgring race')
  plt.tight_layout()
  plt.show()



    # plt.draw()
    # plt.pause(0.000001)
    #plt.clf()

  # fig = plt.figure(figsize=(10, 10))
  # plt.scatter(x, z, s=1)
  # plt.ylim(z_min, z_max)
  # plt.xlim(x_min, x_max)
  # plt.show()
