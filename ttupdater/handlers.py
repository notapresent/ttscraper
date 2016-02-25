import webapp2

import builder
import importers


class IndexTaskHandler(webapp2.RequestHandler):
    """Starts tracker scraping task"""
    def post(self):
        taskmaster = builder.make_taskmaster()
        scraper = builder.make_scraper()
        taskmaster.add_new_torrents(scraper)
        # taskmaster.add_feed_update_task()     # TODO uncomment


class TorrentTaskHandler(webapp2.RequestHandler):
    """Starts individual torrent import task"""
    def post(self):
        param_keys = ['tid', 'title', 'timestamp', 'nbytes']
        params = {key: self.request.get(key) for key in param_keys}
        scraper = builder.make_scraper()
        importers.import_torrent(scraper, params)


class UpdateFeedsTaskHandler(webapp2.RequestHandler):
    def post(self):
        pass    # TODO


class DailyCleanupTaskHandler(webapp2.RequestHandler):
    def post(self):
        pass    # TODO


class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        env = self.request.environ.items()
        self.response.headers['Content-Type'] = 'text/plain'
        env_vars = ["%s: %s" % (k, v) for k, v in env]
        self.response.out.write("\n".join(env_vars))
