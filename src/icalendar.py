#!/usr/bin/env python
from __future__ import print_function
from hashlib import sha1
from datetime import datetime


class Event(object):
    FMT = """BEGIN:VEVENT
        UID:{hashval}
        DTSTART;TZID={time_zone}:{start_time}
        DTEND;TZID={time_zone}:{end_time}
        SUMMARY:{summary}
        END:VEVENT""".replace(' ', '')

    def __init__(self, start, end, summary):
        def format_time(t):
            if isinstance(t, datetime):
                return t.strftime("%Y%m%dT%M%H%SZ")
            return t

        self.start_time = format_time(start)
        self.end_time = format_time(end)
        self.summary = summary

    def str_val(self, tz):
        return Event.FMT.format(
            hashval=self.hash_val(),
            time_zone=tz,
            start_time=self.start_time,
            end_time=self.end_time,
            summary=self.summary
        )

    def hash_val(self):
        return sha1(self.start_time + self.end_time + self.summary).hexdigest()


class ICalendar(object):
    HEAD_FMT = """BEGIN:VCALENDAR
        VERSION:2.0
        X-WR-TIMEZONE:{time_zone}
        BEGIN:VTIMEZONE
        TZID:{time_zone}
        X-LIC-LOCATION:{time_zone}
        END:VTIMEZONE""".replace(' ', '')
    TAIL_FMT = """END:VCALENDAR"""

    def __init__(self, tz, events=None):
        self.tz = tz
        self.events = events or []

    def __str__(self):
        return "\n".join([
            ICalendar.HEAD_FMT.format(time_zone=self.tz),
            "\n".join(event.str_val(self.tz) for event in self.events),
            ICalendar.TAIL_FMT
        ])


if __name__ == '__main__':
    event = Event(
        '20121011T000000Z',
        '20121016T000000Z',
        'Jim and Missy visit NYC'
    )
    cal = ICalendar(tz="America/New_York", events=[event])
    print(str(cal))

    event = Event(
        datetime(2012, 10, 11, 0, 0, 0),
        datetime(2012, 10, 16, 0, 0, 0),
        'Jim and Missy visit NYC'
    )
    cal = ICalendar(tz="America/New_York", events=[event])
    print(str(cal))
