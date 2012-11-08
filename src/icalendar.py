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

    def __init__(self, start_time, end_time, summary):
        def format_time(t):
            if isinstance(t, datetime):
                return t.strftime("%Y%m%dT%H%M%SZ")
            return t

        self.start_time = format_time(start_time)
        self.end_time = format_time(end_time)
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
        args = [self.start_time, self.end_time, self.summary]
        key = "".join(arg.encode('ascii', 'ignore') for arg in args)
        return sha1(key).hexdigest()


class Calendar(object):
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
            Calendar.HEAD_FMT.format(time_zone=self.tz),
            "\n".join(event.str_val(self.tz) for event in self.events),
            Calendar.TAIL_FMT
        ])
