import datetime


def datetime_to_timestamp(dt):
    """Convert naive datetime to POSIX timestamp"""
    return (dt - datetime.datetime(1970, 1, 1)) / datetime.timedelta(seconds=1)
