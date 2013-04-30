import datetime
import json
import sys
sys.path.append('../py-NASA-horizons/source')
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


def test_convert_to_NASA_date2():
    """test for correct conversion"""
    foo = NASAhorizons()
    pythondate = datetime.date(year=1977, month=9, day=10)
    assert "1977-Sep-10" == foo.convert_to_NASA_date(pythondate)


def test_convert_NASA_to_ISO_datestring1():
    """test for non-string rejection"""
    foo = NASAhorizons()
    with pytest.raises(TypeError):
        foo.convert_NASA_to_ISO_datestring(23)
#def test_get_data0():
#    """get (fake) data"""
#    foo = NASAhorizons()
#    assert '[{"x": 23}, {"y": 42}]' == foo.get_data()


def test_get_data1():
    """test for wrong year ordering"""
    foo = NASAhorizons()
    foo.set_object_id(199)
    start = datetime.date(year=1978, month=9, day=10)
    end = datetime.date(year=1977, month=9, day=10)
    with pytest.raises(ValueError):
        foo.get_data(start, end)


def test_get_data2():
    """test for wrong month ordering"""
    foo = NASAhorizons()
    start = datetime.date(year=1977, month=9, day=10)
    end = datetime.date(year=1977, month=8, day=10)
    with pytest.raises(ValueError):
        foo.get_data(start, end)


def test_get_data3():
    """test for wrong day ordering"""
    foo = NASAhorizons()
    foo.set_object_id(199)
    start = datetime.date(year=1977, month=9, day=11)
    end = datetime.date(year=1977, month=9, day=10)
    with pytest.raises(ValueError):
        foo.get_data(start, end)


def test_get_data4():
    """test for same date"""
    foo = NASAhorizons()
    foo.set_object_id(199)
    start = datetime.date(year=1977, month=9, day=10)
    end = datetime.date(year=1977, month=9, day=10)
    foo.get_data(start, end)
