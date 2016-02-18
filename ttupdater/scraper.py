from models import Torrent

class Scraper(object):
    """Extracts torrent data from tracker"""
    def get_new_torrents(self):
        """Returns list of torent entries for new torrents"""
        pass

    def get_torrent_data(self, tid):
        """Returns data for torrent, specified by tid"""
        pass
