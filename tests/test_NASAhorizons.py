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
    foo.create_telnetsession()


def test_close_session():
    """test to close the session
    explicily test for non-existence at the end"""
    foo = NASAhorizons()
    foo.close_session()
    assert foo.has_session() is False
