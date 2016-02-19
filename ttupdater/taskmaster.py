from google.appengine.api.taskqueue import Queue, Task


class TaskMaster(object):
    """Creates and enqueues tasks"""
    def __init__(self):
        self.queue = Queue()

    def add_feed_update_task(self):
        """Enqueue task updating feeds"""
        self.queue.add(Task(url='/tasks/update_feeds'))

    def add_torrent_task(self, torrent_entry):
        """"Enqueue task for torrent entry represented by parser.TorrentEntry named tuple"""
        task = Task(url='/tasks/torrent',params=torrent_entry)
        self.queue.add(task)

    def add_new_torrents(self, scraper):
        """Enqueues tasks for all new torrents"""
        new_entries = scraper.get_new_torrents()
        for e in new_entries:
            self.add_torrent_task(e)
