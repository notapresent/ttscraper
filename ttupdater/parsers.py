"""Everythong related to parsing tracker responses"""
from collections import namedtuple


# Represents one torrent entry from tracker index page
TorrentEntry = namedtuple('TorrentEntry', 'tid,title,timestamp,nbytes')

