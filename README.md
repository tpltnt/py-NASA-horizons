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
* [RFC 4180 - CSV](http://tools.ietf.org/html/rfc4180.html)
* [RFC 4627 - JSON](http://tools.ietf.org/html/rfc4627) and [json.org](http://json.org/)
* [pytest testing framework](http://www.pytest.org)