#!/usr/bin/env python

from sys import argv
from datetime import datetime
import re

from src.icalendar import Event


months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

tuples = \
    [(12, 'a')] + [(h, 'a') for h in range(1, 12)] + \
    [(12, 'p')] + [(h, 'p') for h in range(1, 12)]
trans_12_to_24 = {t: hour for t, hour in zip(tuples, range(24))}


def translate_time(s):
    key = int(s[:-1]), s[-1:]
    return (trans_12_to_24[key], 0, 0)


def translate_time_range(s, e):
    if not s and not e:
        return ((0, 0, 0), (23, 59, 59))
    else:
        return translate_time(s), translate_time(e)


TIME_RANGE = re.compile(r'''
    ^
    (?P<day_of_month>\d+)
    (\s+ (?P<start_time>\d+(a|p)) \- (?P<end_time>\d+(a|p)))?
    \s+ (?P<msg>.*)
    $
''', re.VERBOSE)

DATE_RANGE = re.compile(r'''
    ^
    (?P<start_day>\d+) \- (?P<end_day>\d+)
    \s+ (?P<msg>.*)
    $
''', re.VERBOSE)


def prefixed_msg(msg, prefix):
    return "%s: %s" % (prefix, msg) if prefix else msg


def event_from_date_range(d, year, month, prefix):
    start_day, end_day = (int(d[k]) for k in ('start_day', 'end_day'))
    start_time = datetime(year, month, start_day, 0, 0, 0)
    end_time = datetime(year, month, end_day, 23, 59, 59)
    assert start_time < end_time
    return {
        'start_time': start_time,
        'end_time': end_time,
        'summary': prefixed_msg(d['msg'], prefix),
    }


def event_from_time_range(d, year, month, prefix):
    day = int(d['day_of_month'])
    (start_hour, start_min, start_sec), (end_hour, end_min, end_sec) = \
        translate_time_range(* [d.get(k) for k in ('start_time', 'end_time')])
    start_day, end_day = day, day + int(end_hour < start_hour)
    start_time = datetime(
        year, month, start_day,
        start_hour, start_min, start_sec)
    end_time = datetime(
        year, month, end_day,
        end_hour, end_min, end_sec)
    assert start_time < end_time
    return {
        'start_time': start_time,
        'end_time': end_time,
        'summary': prefixed_msg(d['msg'], prefix),
    }


def create_events(arg, prefix=None):
    events = []
    today = datetime.today()
    year, month = today.year, today.month
    with open(arg) as f:
        lines = filter(None, [line.rstrip() for line in f])
    for line in lines:
        try:
            month = months.index(line[:3].title()) + 1
            if month == 1:
                year += 1
        except ValueError:
            m1 = TIME_RANGE.match(line)
            m2 = DATE_RANGE.match(line)
            if m1:
                event = event_from_time_range(
                    m1.groupdict(),
                    year, month,
                    prefix)
                events.append(event)
            elif m2:
                event = event_from_date_range(
                    m2.groupdict(),
                    year, month,
                    prefix)
                events.append(event)
    return [Event(** e) for e in events]


if __name__ == '__main__':
    from src.icalendar import Calendar

    for arg in argv[1:]:
        events = create_events(arg, "Lori")
        cal = Calendar("America/New_York", events)
        print(str(cal))
