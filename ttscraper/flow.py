"""Orchestrates import process flow"""
import datetime

import dao


def start(taskmaster, scraper):
    """Initiate torrent import process"""
    taskmaster.add_new_torrents(scraper)
    taskmaster.add_feed_update_task()   # TODO only run if there were torrent tasks


def old_import_torrent(torrent_data, scraper):
    """Run torrent import task for torrent, specified by torrent_data"""
    tid = int(torrent_data.pop('tid'))
    torrent_data.update(scraper.get_torrent_data(tid))  # TODO handle 'torrent deleted' and other errors here
    torrent_key = dao.torrent_key(torrent_data.pop('categories'), tid)
    dao.save_torrent(torrent_key, prepare_torrent(torrent_data))


def import_torrent3(torrent_data, scraper):
    tid = int(torrent_data.pop('tid'))
    torrent_data.update(scraper.get_torrent_data(tid))  # TODO handle 'torrent deleted' and other errors here
    torrent_data = prepare_torrent(torrent_data)
    cat_key = dao.category_key_from_tuples(torrent_data['categories'])
    torrent = dao.make_torrent(cat_key, torrent_data)
    to_write = [torrent]

    new_cats = process_categories(cat_key, torrent_data['categories'])

    dao.write_multi(to_write)


def process_categories(cat_key, cat_tuple_list):    # XXX fix this?
    cat = dao.get_from_key(cat_key)

    if cat and cat.dirty:
        return []

    elif cat and not cat.dirty:
        cat.dirty = True
        return [cat]

    else:
        return make_categories(cat_key, cat_tuple_list)


make_categories(cat_tuples):
    tuples_copy = list(cat_tuples)
    rv = []

    while tuples_copy:
        key = dao.category_key_from_tuples(tuples_copy)
        cat = key.get()
        if cat:
            break
        _, _, cat_title = tuples_copy.pop()
        cat = dao.make_category(key, cat_title)
        rv.append(cat)

    return rv

def prepare_torrent(torrent_data):      # TODO move this
    """Prepare torrent field values"""
    return {
        'id': int(torrent_data['tid']),
        'title': torrent_data['title'],
        'dt': datetime.datetime.utcfromtimestamp(int(torrent_data['timestamp'])),
        'nbytes': int(torrent_data['nbytes']),
        'btih': torrent_data['btih'],
        'description': torrent_data['description']
    }
