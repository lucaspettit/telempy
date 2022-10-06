from salsa20 import Salsa20_xor
from granturismo.utils import ntoh

# https://github.com/Nenkai/PDTools/blob/85f11a67489346c62273ca2f70708b4ed3b44279/PDTools.Crypto/SimulationInterface/SimulatorInterfaceCryptorGT7.cs#L15
class Decrypter(object):
  _KEY = b'Simulator Interface Packet GT7 v' #er 0.0 ... we only need 32-bits
  _BYTE_ORDER = 'little'
  _IV_MASK = 0xDEADBEAF
  _GT7_ID = 0x47375330

  @staticmethod
  def decrypt(buffer: bytearray) -> bytearray:
    iv1 = int.from_bytes(ntoh(buffer[64:68]), byteorder=Decrypter._BYTE_ORDER)
    iv2 = iv1 ^ Decrypter._IV_MASK

    iv = bytearray()
    iv.extend(iv2.to_bytes(4, Decrypter._BYTE_ORDER))
    iv.extend(iv1.to_bytes(4, Decrypter._BYTE_ORDER))

    return Salsa20_xor(bytes(buffer), bytes(iv), Decrypter._KEY)
