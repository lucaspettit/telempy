from granturismo.intake import Listener
import sys

if __name__ == '__main__':
  ip_address = sys.argv[1]
  with Listener(ip_address) as listener:
    print(listener.get())
