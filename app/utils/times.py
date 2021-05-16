import time


def pack_date_string(days, months, years):
    return f"{years}-{months}-{days}"


def get_unix_time(date):
    return time.mktime(time.strptime(f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S"))
