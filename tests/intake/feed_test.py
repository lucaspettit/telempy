import json
import queue
import threading

from granturismo.model.packet import Packet
from granturismo import Feed
from tests.helpers import dict2packet, packet2dict
from tests.test_base import TestBase
from unittest.mock import patch, MagicMock
from threading import Event
from queue import Queue
import sure, time


ROOT_DIR = 'granturismo.intake.feed'

class SessionTest(TestBase):
  mock_packets: [dict] = None

  def get_mock_packets(self) -> [Packet]:
    if self.mock_packets is None:
      with open(self._settings.project_directory().joinpath('tests', 'data', 'mock_packet_stream.json')) as f:
        packets = json.load(f)
        for i, p in enumerate(packets):
          p['received_time'] = i
          packets[i] = dict2packet(p)
        self.mock_packets = packets

    return self.mock_packets

  @patch(f'{ROOT_DIR}.socket.socket', name='socket')
  @patch(f'{ROOT_DIR}.Decrypter', name='Decrypter')
  @patch(f'{ROOT_DIR}.Packet', name='Packet')
  def test_session_successfully_streams(self, *mocks):
    packets = self.get_mock_packets()
    mocks = self.unpack_mocks(*mocks)
    socket = MagicMock(name='socket_object')
    decrypter = MagicMock(name='decrypter')
    decrypter.decrypt.return_value = b'fake decrypted value'
    mocks['socket'].return_value = socket
    mocks['Decrypter'].return_value = decrypter
    mocks['Packet'].from_bytes.side_effect = packets

    e = Event()
    q = Queue()

    def recvfrom(buffer_len: int):
      while not e.is_set():
        try:
          value = q.get(timeout=0.1)
          return value
        except queue.Empty:
          continue
      return (b'end', None)

    # mock = MagicMock(name='tuna')
    # mock.recvfrom = MagicMock(name='fish', return_value=('Hello world!', None))
    socket.recvfrom = recvfrom #Mock(name='recvfrom', return_value=(b'0', None))

    sut = Feed('127.0.0.1').start()

    try:
      q.put_nowait((f'fake buffer 1', None))
      time.sleep(0.015)
      actual = packet2dict(sut.get())
      actual.should.eql(packet2dict(packets[0]))

      q.put_nowait((f'fake buffer 2', None))
      time.sleep(0.015)
      actual = packet2dict(sut.get())
      actual.should.eql(packet2dict(packets[1]))

      for i in range(3, 7):
        q.put_nowait((f'fake buffer {i}', None))
        time.sleep(0.015)
      actual = packet2dict(sut.get())
      actual.should.eql(packet2dict(packets[5]))

    finally:
      sock = sut._sock
      sut.close()
      e.set()

    calls = dict(map(lambda x: (x[0], (x[1], x[2])), sock.method_calls))
    calls['setsockopt'].should.eql( ((65535, 4, 1), {}) )
    calls['bind'].should.eql( ((('', 33740),), {}) )
    calls['sendto'].should.eql( ((b'A', ('127.0.0.1', 33739)), {}) )
    calls['close'].should.eql( ((), {}))
