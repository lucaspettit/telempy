import sys

from granturismo.intake import Listener
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':
  ip_address = sys.argv[1]

  # setup the plot styling
  plt.ion()
  fig = plt.figure(figsize=(10, 10))
  plt.xticks([])
  plt.yticks([])

  px, pz = None, None

  prev_time = 0
  with Listener(ip_address) as listener:
    curr_time = time.time()

    # only update graph every 10th of a second just cuz it doesn't matter for us, and it's easier on the computer
    if curr_time - prev_time > 0.1:
      packet = listener.get()

      # note, we're negating z so the map will appear int he same orientation as it does in the game's minimap
      x, z = packet.position.x, -packet.position.z

      if px is not None:
        # here we're adding 3 points on top of each other so that the final point will have the correct coloring for the car's speed range.
        # we're plotting (min speed, max speed, current speed) and matplotlib will adjust the color map so that the final (current speed)
        # color is accurate
        plt.plot([px, x], [pz, z], s=1)

        # pause for a freakishly shot amount of time. We need a pause so that it'll trigger a graph update
        plt.pause(0.00001)

      px, pz = x, z


