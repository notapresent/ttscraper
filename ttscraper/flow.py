"""Orchestrates import process flow"""
import datetime

from taskmaster import TaskMaster
from models import Torrent, Category


def start(taskmaster, scraper):
    """Initiate torrent import process"""
    taskmaster.add_new_torrents(scraper)
    taskmaster.add_feed_update_task()


def import_torrent(torrent_data, scraper):
    """Run torrent import task for torrent, specified by torrent_data"""
    tid = int(torrent_data['tid'])
    torrent_data.update(scraper.get_torrent_data(tid))  # TODO handle 'torrent deleted' and other errors here
    Torrent.save_from_dict(torrent_data)
