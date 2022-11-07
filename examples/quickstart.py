from granturismo import Feed
import sys

if __name__ == '__main__':
  ip_address = sys.argv[1]
  with Feed(ip_address) as feed:
    print(feed.get())
