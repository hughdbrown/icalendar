import unittest
from datetime import datetime

# from mock import Mock, patch
from nose.tools import (
    # raises, assert_true, assert_false,
    assert_equals
)

from src import Calendar, Event


class TestCalendar(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equal_events(self):
        tz = "America/New_York"
        event1 = Event(
            '20121011T000000Z',
            '20121016T000000Z',
            'Jim and Missy visit NYC'
        )
        cal1 = Calendar(tz, events=[event1])

        event2 = Event(
            datetime(2012, 10, 11, 0, 0, 0),
            datetime(2012, 10, 16, 0, 0, 0),
            'Jim and Missy visit NYC'
        )
        cal2 = Calendar(tz, events=[event2])

        assert_equals(str(cal1), str(cal2))
