import datetime
import os
import staticstorage


def datetime_to_timestamp(dt):
    """Convert naive datetime to POSIX timestamp"""
    return (dt - datetime.datetime(1970, 1, 1)) / datetime.timedelta(seconds=1)


def debug_dump(filename, content):
    ts = datetime.datetime.utcnow().strftime('%d-%m-%Y_%H-%M-%S')
    path, suffix = os.path.splitext(filename)
    filename = "{}_{}{}".format(path, ts, suffix)

    if type(content) is unicode:
        content = content.encode('utf-8')

    storage = staticstorage.GCSStorage()
    storage.put(filename, content)
