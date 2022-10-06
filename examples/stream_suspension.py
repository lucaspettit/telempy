from granturismo.intake import Listener
from granturismo.model import Wheels
import datetime as dt
import time, sys
import curses

stdscr = curses.initscr()

def report_suspension(wheels: Wheels) -> None:
  pad = ' ' * 100
  curr_time = dt.datetime.fromtimestamp(time.time()).isoformat()
  stdscr.addstr(0, 0, f'[{curr_time}] Suspension Height{pad}')
  stdscr.addstr(1, 0, f'\t{wheels.front_left.suspension_height:.3f}    {wheels.front_right.suspension_height:.3f}{pad}')
  stdscr.addstr(2, 0, f'\t{wheels.rear_left.suspension_height:.3f}    {wheels.rear_right.suspension_height:.3f}{pad}')
  stdscr.refresh()

if __name__ == '__main__':
  ip_address = sys.argv[1]
  listener = Listener(ip_address)

  try:
    while True:
      packet = listener.get()

      if not packet.flags.loading_or_processing and not packet.flags.paused:
        report_suspension(packet.wheels)
  finally:
    curses.echo()
    curses.nocbreak()
    curses.endwin()
