# coding: utf-8
"""Everythong related to parsing tracker responses"""
import urlparse
from lxml import etree, cssselect

from util import debug_dump


class BaseParser(object):
    """Abstract base class for tracker response parser"""
    def parse_index(self, html):
        """Parse index html and return list of dicts"""
        raise NotImplementedError()

    def parse_torrent_page(self, html):
        """Parse torrent page and return dict"""
        raise NotImplementedError()


def btih_from_href(url):
    """Extracts infohash from magnet link"""
    parsed = urlparse.urlparse(url)
    params = urlparse.parse_qs(parsed.query)
    xt = params['xt'][0]
    return xt[9:]


def make_tree(html):
    """Make lxml.etree from html"""
    htmlparser = etree.HTMLParser(encoding='utf-8')
    return etree.fromstring(html, parser=htmlparser)


class Error(RuntimeError):
    """Parse error"""
    pass
