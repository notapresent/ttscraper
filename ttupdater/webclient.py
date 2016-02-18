# coding: utf-8
import requests
from models import Account


class WebClient(object):
    """Comunicates with tracker via HTTP"""
    TRACKER_HOST = 'rutracker.org'
    INDEX_FORM_DATA = {'prev_new': 0, 'prev_oop': 0, 'f[]': -1, 'o': 1, 's': 2, 'tm': -1, 'oop': 1}

    def __init__(self, session=None, account=None):
        self.session = session or requests.Session()
        self.account = account

    def get_torrent_page(self, tid):
        """"Returns torrent page content"""
        url = self.torrent_page_url(tid)
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.text

    def torrent_page_url(self, tid):
        """Returns torrent page url"""
        return 'http://{}/forum/viewtopic.php?t={}'.format(self.TRACKER_HOST, tid)

    def get_index_page(self):
        """Returns page with latest torrents list"""
        url = 'http://{}/forum/tracker.php'.format(self.TRACKER_HOST)
        resp = self.user_request('POST', url, data=self.INDEX_FORM_DATA)

        resp.raise_for_status()
        if isinstance(resp.text, basestring) and not self.is_logged_in(resp.text):
            raise RuntimeError('{} - Cookie login failed'.format(self.account))

        return resp.text

    def log_in(self):
        """Sets session cookies from account or via tracker login"""
        if not self.account:
            self.account = Account.get_one()

        if self.account.cookies:
            self.session.cookies.update(self.account.cookies)
        else:
            self.tracker_log_in()
            self.account.cookies = self.session.cookies.get_dict()
            self.account.put()

    def user_request(self, *args, **kwargs):
        """Issue a web request on behalf of tracker user"""
        self.log_in()
        return self.session.request(*args, **kwargs)    # FIXME Handle cookies expiring

    def tracker_log_in(self):
        """Submit user credentials to tracker"""
        url = 'http://login.{}/forum/login.php'.format(self.TRACKER_HOST)
        data = login_form_data(self.account)

        resp = self.session.post(url, data=data)

        resp.raise_for_status()
        if isinstance(resp.text, basestring) and not self.is_logged_in(resp.text):
            raise RuntimeError('Tracker login failed')

    def is_logged_in(self, html):
        """Checks if page was downloaded with user logged in"""
        return str(self.account.userid) in html


def login_form_data(acc):
    """Helper function to make login form data"""
    return {
        'login_password': acc.password,
        'login_username': acc.username,
        'login': 'Whatever'        # Must be non-empty
    }
