import sys

from granturismo.intake import Listener
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
  ip_address = sys.argv[1]

  # setup the plot styling
  plt.ion()
  fig, ax = plt.subplots(figsize=(10, 10))
  ax.axis('off')
  plt.xticks([])
  plt.yticks([])

  px, pz = None, None

  count = 0
  with Listener(ip_address) as listener:
    while True:
      count += 1
      # only update graph every 10th of a second just cuz it doesn't matter for us, and it's easier on the computer
      # but we still need to grab the packet even if we're not using it
      packet = listener.get()

      if count >= 20:
        count = 0
        # note, we're negating z so the map will appear int he same orientation as it does in the game's minimap
        x, z = packet.position.x, -packet.position.z
        if px is None:
          px = x
          pz = z

        # here we're adding 3 points on top of each other so that the final point will have the correct coloring for the car's speed range.
        # we're plotting (min speed, max speed, current speed) and matplotlib will adjust the color map so that the final (current speed)
        # color is accurate
        speed = min(1, packet.car_speed / packet.car_max_speed) * 3
        print(f'{packet.car_speed:.1f}/{packet.car_max_speed:.1f} = {speed=}')
        color = plt.cm.plasma(speed)
        plt.plot([px, x], [pz,  z], color=color)
        plt.gca().set_aspect('equal', adjustable='box')

        # pause for a freakishly shot amount of time. We need a pause so that it'll trigger a graph update
        plt.pause(0.00000000000000000001)

        px, pz = x, z


