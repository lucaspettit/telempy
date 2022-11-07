from tests.test_base import TestBase
from granturismo.security import Decrypter as sut
from typing import Tuple
import sure


class DecrypterTest(TestBase):
  def get_input_output(self) -> Tuple[bytearray, bytearray]:
    with open(self._settings.project_directory().joinpath('tests', 'data', 'rawUdpMessage1.bytes'), 'rb') as f:
      input_packet = bytearray(f.read())
    with open(self._settings.project_directory().joinpath('tests', 'data', 'decryptedUdpMessage1.bytes'), 'rb') as f:
      output_packet = bytearray(f.read())
    return input_packet, output_packet

  def test_decrypt(self):
    buffer, expected = self.get_input_output()
    actual = sut.decrypt(buffer)
    actual.should.eql(expected)
