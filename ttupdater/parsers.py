# coding: utf-8
"""Everythong related to parsing tracker responses"""
# TODO rename this module to avoid conflicts with stdlib parser
from collections import namedtuple
from lxml import etree, cssselect


# Represents one torrent entry from tracker index page
TorrentEntry = namedtuple('TorrentEntry', 'tid,title,ts,nbytes')


class BaseParser(object):
    """Abstract base class for tracker response parser"""
    def parse_index(self, html):
        """Parse index html and return list of TorrentEntry"""
        raise NotImplementedError()

    def parse_torrent_page(self, html):
        """Parse torrent page and return dict"""
        raise NotImplementedError()


class Parser(BaseParser):
    def parse_index(self, html):
        rows = self.parse_index_table(html)
        return [self.parse_index_row(row) for row in rows]

    def parse_index_table(self, html):
        tree = make_tree(html)
        """Returns list of index rows represented as etree.Elements"""
        rows_selector = cssselect.CSSSelector('table#tor-tbl tr.tCenter.hl-tr')
        return rows_selector(tree)

    def parse_index_row(self, row):
        """Parse index row represented by lxml element and return TorrentEntry"""
        tid = self.index_tid(row)
        title = self.index_title(row)
        ts = self.index_timestamp(row)
        nbytes = self.index_nbytes(row)

        return TorrentEntry(tid, title, ts, nbytes)

    def index_tid(self, elem):
        title_link_selector = cssselect.CSSSelector('td.t-title div.t-title a')
        a = title_link_selector(elem)[0]
        tid = a.attrib['data-topic_id']
        return int(tid)

    def index_title(self, elem):
        title_link_selector = cssselect.CSSSelector('td.t-title div.t-title a')
        a = title_link_selector(elem)[0]
        return a.text

    def index_timestamp(self, elem):
        timestamp_selector = cssselect.CSSSelector('td:last-child u')
        timestamp = timestamp_selector(elem)[0].text
        return int(timestamp)

    def index_nbytes(self, elem):
        nbytes_selector = cssselect.CSSSelector('td.tor-size u')
        nbytes = nbytes_selector(elem)[0].text
        return int(nbytes)


def make_tree(html):
    """Make lxml.etree from html"""
    htmlparser = etree.HTMLParser(encoding='utf-8')
    return etree.fromstring(html, parser=htmlparser)
