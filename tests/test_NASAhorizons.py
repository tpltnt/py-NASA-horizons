import sys
sys.path.append('../py-NASA-horizons')
import pytest
from NASAhorizons import NASAhorizons


def test_init0():
    """test object construction"""
    foo = NASAhorizons()


def test_create_telnetsession():
    """test to create a telnet session. This should not time out."""
    foo = NASAhorizons()
    foo.create_telnetsession()
