"""Orchestrates import process flow"""
import datetime

import dao


def start(taskmaster, scraper):
    """Initiate torrent import process"""
    taskmaster.add_new_torrents(scraper)
    taskmaster.add_feed_update_task()


def import_torrent(torrent_data, scraper):
    """Run torrent import task for torrent, specified by torrent_data"""
    tid = int(torrent_data.pop('tid'))
    torrent_data.update(scraper.get_torrent_data(tid))  # TODO handle 'torrent deleted' and other errors here
    tk = dao.torrent_key(torrent_data.pop('categories'), tid)
    ts = int(torrent_data.pop('timestamp'))
    torrent_data['dt'] = datetime.datetime.utcfromtimestamp(ts)
    torrent_data['nbytes'] = int(torrent_data['nbytes'])
    dao.save_torrent(tk, torrent_data)
