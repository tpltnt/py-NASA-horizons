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



def test_has_session():
    """vanilla object should not have a session"""
    foo = NASAhorizons()
    assert foo.has_session() is False


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


def test_get_data0():
    """known good test (also in docs)"""
    foo = NASAhorizons()
    foo.set_object_id(199)
    start = datetime.date(year=1977, month=9, day=10)
    end = datetime.date(year=1977, month=9, day=12)
    returndata = [
        {'z': -0.02967482538878673,
         'y': 0.02365967857453419,
         'x': 0.3497488933057855,
         'date': '1977-09-10T00:00:00.0000'},
        {'z': -0.02647449350730847,
         'y': 0.05283430192085586,
         'x': 0.3408485768468899,
         'date': '1977-09-11T00:00:00.0000'},
        {'z': -0.02308289285966815,
         'y': 0.08159238988582097,
         'x': 0.3294953295232826,
         'date': '1977-09-12T00:00:00.0000'}]
    assert returndata == foo.get_data(start, end, format="list")


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
    """test for same date/query one day"""
    foo = NASAhorizons()
    foo.set_object_id(199)
    start = datetime.date(year=1977, month=1, day=1)
    end = datetime.date(year=1977, month=1, day=1)
    returndata = [
        {'z': 0.01562549439448472,
         'y': 0.2894764150799116,
         'x': 0.09117860868439513,
         'date': '1977-01-01T00:00:00.0000'}]
    assert returndata == foo.get_data(start, end)
