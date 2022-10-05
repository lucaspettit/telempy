import json
from src.intake.listener import UDPServer
from src.security.decrypter import Decrypter
from src.models.packet import unpack
from pathlib import Path
from argparse import ArgumentParser
from pprint import pprint

def parseargs():
  parser = ArgumentParser()
  parser.add_argument('-t', '--track', type=str, required=True,
                    help='The track name as it appears in Gran Truismo')
  return parser.parse_args()


if __name__ == '__main__':
  odir = Path('/data/trackDataRaw')
  odir.mkdir(parents=True, exist_ok=True)
  track_id = len(list(odir.glob('*.json')))

  count = 0
  race_started = False
  finished = False
  #args = parseargs()
  track_name = 'Daytona International Speedway' #args.track
  layout = None

  packets = []
  decryter = Decrypter()
  listener = UDPServer()

  if layout is not None:
    print(f'[{track_name} - {layout}]')
  else:
    print(f'[{track_name}]')
  print(f'\tWaiting for race to start')


  def handler(buffer: bytes) -> bool:
    global count, finished, race_started, prev_position
    packet = unpack(decryter.decrypt(buffer))

    # time trials will have lapsInRace == 0
    # circuit experience sectors will have lapsInRace == 1 && lapCount == 2
    # menu screen will have lapCount == 65535
    if packet['flags']['loadingOrProcessing']:
      in_race = False
    elif packet['lapCount'] == 1 and packet['lapsInRace'] == 0: # were in a time trial first lap
      in_race = True
    else:
      in_race = packet['lapCount'] != 65535 \
          and (packet['lapCount'] <= 1) \
          and (packet['lapsInRace'] > 0 and
        packet['lapsInRace'] >= packet['lapCount'])


    if not in_race and not race_started:
      # race hasn't started yet!
      return False

    if in_race and not race_started:
      # the race has started!
      print(f'\tRace started! capturing packets now')
      race_started = True

    if not in_race and finished:
      # we've already saved the packets
      return False

    if not in_race and race_started and not finished:
      if count < 10:
        print(f'\tFalse start. Resetting conditions. packetCount:[{count}]')
        count = 0
        finished = False
        race_started = False
        return False

      # the race ended, save the data
      _packets = list(filter(lambda p: p['lapCount'] == 1, packets))
      print(f'\tRace ended. Captured {len(_packets)}. Saving telemetry data')
      filename = odir.joinpath(f'{track_name} - {layout}.json') if layout is not None else odir.joinpath(f'{track_name}.json')
      print(f'\tWriting to file {filename}')
      with open(filename, 'w') as f:
        json.dump({
          'track': {
            'id': track_id,
            'name': track_name,
            'layout': layout,
          },
          'packets': _packets
        }, f)
      finished = True
      return True

    packets.append({
      'position': packet['position'],
      'orientation': packet['orientation'],
      'lapCount': packet['lapCount']
    })
    count += 1
    return False


  listener.add_handler(handler)
  listener.listen()