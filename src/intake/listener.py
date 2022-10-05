import socket
import time
import datetime as dt
import threading
import signal
from typing import Dict, Union, Callable, List

class Listener(object):
  _HEARTBEAT_PORT = 33739
  _BIND_PORT = 33740
  _BUFFER_LEN = 0x128  # in bytes
  _HEARTBEAT_DELAY = 10 # in seconds
  _HEARTBEAT_MESSAGE = b'A'

  def __init__(self, addr: str):
    """
    Initialize the telemetry listener
    :param addr: Address to the PlayStation so we can send a heartbeat
    """
    self._attr = addr
    self._sock = self._init_sock_(self._BIND_PORT)
    self._handlers: List[Callable] = []

    self._terminate_event = threading.Event()
    signal.signal(signal.SIGINT, lambda *args: self._terminate_event.set())
    signal.signal(signal.SIGTERM, lambda *args: self._terminate_event.set())
    self._heartbeat_thread = threading.Thread(target=self._send_heartbeat)
    self._heartbeat_thread.start()

  def add_handler(self, h: Callable) -> None:
    self._handlers.append(h)

  def get(self) -> bytes:
    packet = self._read_udp(self._sock)
    if packet['status'] == -1:
      print(f'  \u001b[31mFailed to retrieve message on {self._BIND_PORT}\u001b[0m')
    elif packet['status'] == -2:
      print(f'  \u001b[33mTimedout waiting for message on {self._BIND_PORT}\u001b[0m')
    elif packet['status'] != 0:
      print(f'  \u001b[33mUnknown status:[{packet["status"]}]')
    else:
      return packet['body']

  def _send_heartbeat(self) -> None:
    last_heartbeat = 0
    while not self._terminate_event.is_set():
      curr_time = time.time()
      if curr_time - last_heartbeat >= self._HEARTBEAT_DELAY:
        last_heartbeat = curr_time
        timestamp = dt.datetime.fromtimestamp(curr_time).isoformat().split(".", 1)[0]
        print(f'[{timestamp}] Sending heartbeat')
        self._sock.sendto(self._HEARTBEAT_MESSAGE, (self._attr, self._HEARTBEAT_PORT))
      time.sleep(0.01)

  @staticmethod
  def _init_sock_(port: int, addr: str='') -> socket.socket:
    # Create a datagram socket
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    # Enable immediate reuse of IP address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    sock.bind((addr, port))
    # Set a timeout so the socket does not block indefinitely when trying to receive data
    sock.settimeout(0.5)

    return sock

  @staticmethod
  def _read_udp(sock: socket.socket) -> Dict[str, Union[bytearray, str]]:
    try:
      data, addr = sock.recvfrom(Listener._BUFFER_LEN)
    except socket.timeout as e:
      return {'body': bytes(), 'status': -2}
    except Exception as e:
      return {'body': bytes(), 'status': -1, 'error': e}
    else:
      return {'body': data, 'status': 0}
