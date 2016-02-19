from models import Torrent


class Scraper(object):
    def __init__(self, webclient, parser):
        self.webclient = webclient
        self.parser = parser
        self.dt_threshold = None

    """Extracts torrent data from tracker"""
    def get_new_torrents(self):
        """Returns list of torent entries for new torrents"""
        index_html = self.webclient.get_index_page()
        entries = self.parser.parse_index(index_html)
        return [e for entry in entries if self.is_new(e)]

    def get_torrent_data(self, tid):
        """Returns data for torrent, specified by tid"""
        html = self.webclient.get_torrent_page(tid)
        entry = self.parser.parse_torrent_page(html)
        return entry

    def is_new(self, entry):
        """Returns true for new entries, obviously"""
        if not self.dt_threshold:
            self.dt_threshold = Torrent.get_latest_dt()     # TODO not sure where to put this
        return entry.dt >= self.dt_threshold
