from telempy.intake.listener import Listener
from telempy.security.decrypter import Decrypter
from telempy.model.packet import Packet
import json
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint


if __name__ == '__main__':
  decrypter = Decrypter()
  count, packet_count = 0, 0
  pos = {'x': [], 'y': [], 'z': []}
  speed = []

  plt.ion()
  fig = plt.figure(figsize=(10, 10))
  plt.xticks([])
  plt.yticks([])
  xbounds = -775.9378875732422, 694.2568309020996
  zbounds = -1183.405450439453, 1195.2072109985352
  px, pz = None, None
  packets = []

  def f(buffer: bytes) -> None:
    global count, packet_count, px, pz
    count += 1

    # take a 10s sample
    if count % 20 == 0:
      packet = Packet.from_bytes(decrypter.decrypt(buffer))
      packets.append(packet)

      if px is not None or pz is not None:
        plt.plot([px, packet.position.x], [pz, -packet.position.z], 'b')
        plt.pause(0.00000000000000000000000001)
      px, pz = packet.position.x, -packet.position.z

    if count % 3600 == 0:
      with open('packets.json', 'w') as f:
        json.dump(packets, f)


  listener = Listener('192.168.1.207')
  import time
  start_time = time.time()
  while time.time() - start_time < 8:
    packet = listener.get()
  print('ending program')
