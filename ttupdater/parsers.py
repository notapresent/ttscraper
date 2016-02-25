# coding: utf-8
"""Everythong related to parsing tracker responses"""
# TODO rename this module to avoid conflicts with stdlib parser
from lxml import etree, cssselect


class BaseParser(object):
    """Abstract base class for tracker response parser"""
    def parse_index(self, html):
        """Parse index html and return list of dicts"""
        raise NotImplementedError()

    def parse_torrent_page(self, html):
        """Parse torrent page and return dict"""
        raise NotImplementedError()


class Parser(BaseParser):
    def parse_index(self, html):
        rows = self.parse_index_table(html)
        return [self.parse_index_row(row) for row in rows]

    def parse_torrent_page(self, html):
        tree = make_tree(html)
        return {
            'categories': self.torrent_categories(tree),
            'description': self.torrent_description(tree),
            'btih': self.torrent_btih(tree)
        }

    def parse_index_table(self, html):
        tree = make_tree(html)
        """Returns list of index rows represented as etree.Elements"""
        rows_selector = cssselect.CSSSelector('table#tor-tbl tr.tCenter.hl-tr')
        return rows_selector(tree)

    def parse_index_row(self, row):
        """Parse index row represented by lxml element and return dict"""
        tid = self.index_tid(row)
        title = self.index_title(row)
        ts = self.index_timestamp(row)
        nbytes = self.index_nbytes(row)

        return {
            'tid': tid,
            'title': title,
            'timestamp': ts,
            'nbytes': nbytes
            }

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

    def torrent_categories(self, tree):
        cat_selector = cssselect.CSSSelector('td.nav.w100.pad_2.brand-bg-white > span > a')
        cat_links = cat_selector(tree)
        return [self.parse_category_link(elem) for elem in cat_links]

    def parse_category_link(self, link):
        href = link.attrib['href']
        if '=' in href:
            head, tail = href.split('=')
            cat_id = int(tail)
            cat_kind = head[-1]
        else:
            cat_id = 0
            cat_kind = 'r'

        return {
            'id': cat_id,
            'kind': cat_kind,
            'title': link.text
        }

    def torrent_description(self, tree):
        desc_selector = cssselect.CSSSelector('div.post_body')
        elem = desc_selector(tree)[0]
        contents_list = [etree.tostring(e, encoding='utf-8') for e in elem.iterchildren()]
        return ''.join(contents_list)

    def torrent_btih(self, tree):
        btih_selector = cssselect.CSSSelector('span#tor-hash')
        elem = btih_selector(tree)[0]
        return elem.text


def make_tree(html):
    """Make lxml.etree from html"""
    htmlparser = etree.HTMLParser(encoding='utf-8')
    return etree.fromstring(html, parser=htmlparser)


class Error(RuntimeError):
    """Parse error"""
    pass
