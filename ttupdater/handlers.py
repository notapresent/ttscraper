import os
import webapp2

from builder import ObjectBuilder


class IndexTaskHandler(webapp2.RequestHandler):
    """Starts tracker scraping task"""
    def post(self):
        builder = ObjectBuilder()
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


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

task_app = webapp2.WSGIApplication([
    ('/task/index', IndexTaskHandler),
    ('/task/torrent', TorrentTaskHandler),
], debug=debug)

manage_app = public_handler = webapp2.WSGIApplication([
    ('/manage/', DashboardHandler),
], debug=debug)
