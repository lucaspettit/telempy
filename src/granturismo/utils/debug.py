import struct

def to_bit_str(b: [bytes, bytearray, int, str]) -> str:
  if isinstance(b, float):
    b = bytes(struct.pack("f", b))
  if isinstance(b, bytearray):
    b = bytes(b)

  if isinstance(b, bytes):
    s = []
    for c in b:
      s.append(_format(bin(c)))
    return ' '.join(s)
  if isinstance(b, int):
    return _format(bin(b))
  if isinstance(b, str):
    s = []
    for c in b:
      s.append(_format(bin(ord(c))))
    return ' '.join(s)


def _format(s: str) -> str:
  if len(s) >= 2 and s[1] == 'b':
    s = s[2:]
  remainder = len(s) % 8
  remainder = 0 if remainder == 0 else 8 - remainder
  s = ('0' * remainder) + s

  for i in range(len(s) - 8, 0, -8):
    s = s[:i] + ' ' + s[i:]

  return s


if __name__ == '__main__':
  print(to_bit_str(b'\xb1\xdf\x0b\xe9\xb0\xcc\xf8\xa5q'))