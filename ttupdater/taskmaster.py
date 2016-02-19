from google.appengine.api.taskqueue import Queue, Task

# from scraper import Scraper


class TaskMaster(object):
    """Creates and enqueues tasks"""
    def __init__(self, tq=None):
        self.queue = tq or Queue()

    def add_feed_update_task(self):
        """Enqueue task updating feeds"""
        self.queue.add(Task(url='/tasks/update_feeds'))

    def add_torrent_task(self, torrent_entry):
        """"Enqueue task for torrent entry represented by dict-like object"""
        tt = Task(url='/tasks/torrent',params=torrent_entry)
        self.queue.add(tt)

    def add_new_torrents(self, scraper=None):
        """Enqueues tasks for all new torrents"""
        scrp = scraper or Scraper()     # FIXME move this somewhere else

        new_entries = scrp.get_new_torrents()
        for e in new_entries:
            self.add_torrent_task(e)
