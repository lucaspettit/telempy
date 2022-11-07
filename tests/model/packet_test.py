import json
from typing import Tuple

from granturismo.model.packet import Packet
from tests.helpers import packet2dict
from tests.test_base import TestBase
import sure


class PacketTest(TestBase):
  def get_input_output(self) -> Tuple[bytearray, Packet]:
    with open(self._settings.project_directory().joinpath('tests', 'data', 'decryptedUdpMessage1.bytes'), 'rb') as f:
      input_packet = bytearray(f.read())
    with open(self._settings.project_directory().joinpath('tests', 'data', 'packet1.json')) as f:
      output_packet = json.load(f)
    return input_packet, output_packet

  def test_valid_buffer(self):
    buffer, expected = self.get_input_output()

    actual = Packet.from_bytes(buffer, expected['retrieved_time'])
    actual = packet2dict(actual)  # convert to dict because Packet doesn't do == well.
    actual.should.eql(expected)

  def test_invalid_buffer(self):
    buffer, _ = self.get_input_output()
    buffer[0:4] = b'G7S0'  # buffer's in little endian, so this will get swapped to 0S7G
    Packet.from_bytes.when.called_with(buffer, 0) \
      .should.throw(ValueError, 'Token is invalid! Got 0S7G but expected G7S0')
