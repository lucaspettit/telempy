"""
In this example, we are streaming the car's position straight to a Matplotlib plot.
You'll see the plot update as you drive around the track, with the car's path using
a heatmap color to depict the speed.
"""
import sys
from granturismo.intake import Listener
import matplotlib.pyplot as plt

if __name__ == '__main__':
  ip_address = sys.argv[1]

  # setup the plot styling
  plt.ion() # allows us to continue to upate the plot
  fig, ax = plt.subplots(figsize=(8, 8))
  ax.axis('off') # hides the black border around the axis.
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
          px, pz = x, z
          continue

        # here we're getting the ratio of how fast the car's going compared to it's max speed.
        # we're multiplying by 3 to boost the colorization range.
        speed = min(1, packet.car_speed / packet.car_max_speed) * 3
        # Now use the "speed" ratio to select the color from the Matplotlib pallet
        color = plt.cm.plasma(speed)

        # plot the current step
        plt.plot([px, x], [pz,  z], color=color)

        # set the aspect ratios to be equal for x/z axis, this way the map doesn't look skewed
        plt.gca().set_aspect('equal', adjustable='box')

        # pause for a freakishly shot amount of time. We need a pause so that it'll trigger a graph update
        plt.pause(0.00000000000000000001)

        px, pz = x, z
