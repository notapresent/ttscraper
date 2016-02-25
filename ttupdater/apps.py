import os
import webapp2

import handlers


debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

task_app = webapp2.WSGIApplication([
    ('/task/index', handlers.IndexTaskHandler),
    ('/task/torrent', handlers.TorrentTaskHandler),
], debug=debug)

manage_app = webapp2.WSGIApplication([
    ('/manage/', handlers.DashboardHandler),
], debug=debug)
