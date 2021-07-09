import datetime as dt
import time

SECOND_IN_MINUTE = 60
SECOND_IN_HOUR = SECOND_IN_MINUTE * 60
SECOND_IN_DAY = SECOND_IN_HOUR * 24

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = dt.datetime.fromtimestamp(now_timestamp) - dt.datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset

def datetime_from_local_to_utc(local_datetime):
    now_timestamp = time.time()
    offset = dt.datetime.fromtimestamp(now_timestamp) - dt.datetime.utcfromtimestamp(now_timestamp)
    return local_datetime - offset

def get_unix_time(utc_datetime: dt.datetime) -> float:
    return (utc_datetime - dt.datetime(1970, 1, 1)).total_seconds()

def get_current_unix_time() -> float:
    return get_unix_time(dt.datetime.utcnow())

def unix_time_to_iso(unix_time: float):
    return dt.datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")

def get_unix_day_start_time(unix_time = get_current_unix_time()):
    datetime = dt.datetime.fromtimestamp(unix_time)
    return get_unix_time(datetime_from_local_to_utc(dt.datetime.combine(datetime.date(), dt.time(00, 00, 00))))
