from sys import byteorder


_LITTLE = byteorder == 'little'


def ntoh(b: bytearray) -> bytearray:
  """
  Network to host.
  Converts the byte order from the little-endian that we receive from the PS to whatever endian the machine uses
  :param b: the input bytes in little-endian order that PS provides
  :return: the bytes in the correct endian order for the machine
  """
  if _LITTLE:
    return b
  return b[::-1]