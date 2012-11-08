import unittest
import os.path

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
        root = os.path.dirname(__file__)
        datafile = os.path.join(root, 'data', 'lori_cal.txt')
        events = translate_cal.create_events(datafile)
        assert_equals(len(events), 28)
        #ical = Calendar(events)
