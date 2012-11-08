import unittest

# from mock import Mock, patch
from nose.tools import (
    # raises, assert_true, assert_false,
    assert_equals
)

#from src import Calendar
import translate_cal


class TestICalendar(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_events(self):
        events = translate_cal.create_events('data/lori_cal.txt')
        assert_equals(len(events), 28)
        #ical = Calendar(events)
