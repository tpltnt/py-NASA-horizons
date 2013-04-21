import datetime
import json
import sys
sys.path.append('../py-NASA-horizons')
import pytest
from NASAhorizons import NASAhorizons


def test_init0():
    """test object construction"""
    foo = NASAhorizons()


def test_init1():
    """test if object construction already creates a session (as expected)."""
    foo = NASAhorizons()
    assert foo.has_session() is True


def test_create_telnetsession():
    """test to create a telnet session. This should not time out."""
    foo = NASAhorizons()
    foo.create_session()


def test_close_session():
    """test to close the session
    explicily test for non-existence at the end"""
    foo = NASAhorizons()
    foo.close_session()
    assert foo.has_session() is False


def test_set_object_id0():
    """test to set object id (Voyager I = -31)"""
    foo = NASAhorizons()
    foo.set_object_id(-31)


def test_set_object_id1():
    """test for non-integer id rejection (string)"""
    foo = NASAhorizons()
    with pytest.raises(TypeError):
        foo.set_object_id('-31')


def test_set_object_id1000():
    """temporary test to catch unfullfillable requests."""
    foo = NASAhorizons()
    with pytest.raises(NotImplementedError):
        foo.set_object_id(23)


def test_convert_to_NASA_date0():
    """test for accepting datetime.date objects"""
    foo = NASAhorizons()
    pythondate = datetime.date(year=1977, month=9, day=10)
    foo.convert_to_NASA_date(pythondate)


def test_convert_to_NASA_date1():
    """test for rejecting non-datetime.date objects (string)"""
    foo = NASAhorizons()
    with pytest.raises(TypeError):
        foo.convert_to_NASA_date("1977-09-10")
#def test_get_data0():
#    """get (fake) data"""
#    foo = NASAhorizons()
#    assert '[{"x": 23}, {"y": 42}]' == foo.get_data()
