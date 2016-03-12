# coding: utf-8
"""Webclient is responsible for comunicating with tracker via HTTP"""
import logging
import requests

from models import Account


TIMEOUTS = (3.05, 10)       # Connect, read


class BaseWebClient(object):
    """Base class for tracker adapters"""
    ENCODING = 'utf-8'      # Default encoding for text responses

    def __init__(self, session=None):
        self.session = session or requests.Session()
        # Set logging level for libraries
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def request(self, url, method='GET', **kwargs):
        """Send an actual http request, raise Error on error"""
        try:
            resp = self.session.request(method, url, timeout=TIMEOUTS, **kwargs)
            if not resp.ok:
                resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise RequestError(str(e))

        return resp

    def user_request(self, account, url, method='GET',  **kwargs):
        """Send request on behalf of tracker user, handle session cookies"""
        if account.cookies:
            self.session.cookies.update(account.cookies)
        else:
            self.tracker_log_in(account)
            account.cookies = self.session.cookies.get_dict()

        try:
            resp = self.authorized_request(account, url, method,  **kwargs)
        except NotLoggedIn as e:
            account.cookies = None
            raise

        return resp

    def authorized_request(self, account, url, method,  **kwargs):
        """Issue HTTP request and raise NotLoggedIn if user was not authorised on server"""
        resp = self.request(url, method, **kwargs)
        html = self.get_text(resp)

        if html and not self.is_logged_in(html, account):
            raise NotLoggedIn('User {} is not logged in'.format(account))

        return resp

    def get_text(self, response):
        """Returns response text for text responses, None for non-text"""
        if 'text' in response.headers['content-type']:
            response.encoding = self.ENCODING
            return response.text

    def is_logged_in(self, html, account):
        """Returns true if html response has user account info"""
        return account.userid in html



class Error(RuntimeError):
    """Base class for all exceptions in this module"""
    pass


class RequestError(Error):
    """HTTP-level error"""
    pass


class LoginFailed(Error):
    """Server login failed"""
    pass


class NotLoggedIn(Error):
    """User is not logged in"""
    pass
