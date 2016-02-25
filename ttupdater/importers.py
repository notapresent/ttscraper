import datetime

import webclient
from models import Torrent, Category


def import_torrent(scraper, torrent_data):
    tid = int(torrent_data['tid'])
    title = torrent_data['title']
    dt = datetime.datetime.utcfromtimestamp(int(torrent_data['timestamp']))
    nbytes = int(torrent_data['nbytes'])
    more_data = scraper.get_torrent_data(tid)        # TODO handle 'torrent deleted' here
    btih = more_data['btih']

    Torrent.save_torrent(tid, title, btih, dt, nbytes)
