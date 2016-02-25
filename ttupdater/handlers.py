import webapp2

import builder


class IndexTaskHandler(webapp2.RequestHandler):
    """Starts tracker scraping task"""
    def post(self):
        taskmaster = builder.make_taskmaster()
        scraper = builder.make_scraper()
        taskmaster.add_new_torrents(scraper)
        taskmaster.add_feed_update_task()


class TorrentTaskHandler(webapp2.RequestHandler):
    """Starts individual torrent import task"""
    def post(self):
        pass


class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        env = self.request.environ.items()
        self.response.headers['Content-Type'] = 'text/plain'
        env_vars = ["%s: %s" % (k, v) for k, v in env]
        self.response.out.write("\n".join(env_vars))
