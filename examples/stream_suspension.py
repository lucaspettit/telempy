from granturismo.intake import Listener
from granturismo.model import Wheels
import datetime as dt
import time, sys
import curses

stdscr = curses.initscr()

# This function is used to rewrite multiple lines on the terminal
def report_suspension(wheels: Wheels) -> None:
  curr_time = dt.datetime.fromtimestamp(time.time()).isoformat()
  stdscr.addstr(0, 0, f'[{curr_time}] Suspension Height')
  stdscr.addstr(1, 0, f'\t{wheels.front_left.suspension_height:.3f}    {wheels.front_right.suspension_height:.3f}')
  stdscr.addstr(2, 0, f'\t{wheels.rear_left.suspension_height:.3f}    {wheels.rear_right.suspension_height:.3f}')
  stdscr.refresh()

if __name__ == '__main__':
  ip_address = sys.argv[1]

  # To use the Listener session without a `with` clause, you'll need to call the `.start()` function.
  listener = Listener(ip_address)
  listener.start()

  try:
    while True:
      # get the latest packet from PlayStation
      packet = listener.get()

      # If the game isn't paused or in a loading state, we'll update the terminal with the latest suspension info.
      if not packet.flags.loading_or_processing and not packet.flags.paused:
        report_suspension(packet.wheels)
  finally:
    # If you don't use a `with` clause, then you'll need to close the session afterwords. Session will also successfully close with CTRL+C
    curses.echo()
    curses.nocbreak()
    curses.endwin()
    listener.close()
