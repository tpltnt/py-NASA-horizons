import sys
sys.path.append('../py-NASA-horizons')
import pytest
from NASAhorizons import NASAhorizons


def test_init0():
    """test object construction"""
    foo = NASAhorizons()
