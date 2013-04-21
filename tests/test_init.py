import sys
sys.path.append('../py-NASA-horizons')
import pytest
from py-NASA-horizons import NASAhorizons


def test_init0():
    """test object construction"""
    foo = NASAhorizons()

