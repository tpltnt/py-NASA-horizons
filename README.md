py-NASA-horizons
================

A pure python3 wrapper for JPL HORIZONS on-line solar system data and ephemeris computation service.
It uses the telnet interface.

current strategy: set up a context to query (object and daterange) and
retrieve data from it.


references
==========
* [NASA HORIZONS page](http://ssd.jpl.nasa.gov/?horizons)
* [RFC 854 - telnet](http://tools.ietf.org/html/rfc854.html)
* [pytest testing framework](http://www.pytest.org)