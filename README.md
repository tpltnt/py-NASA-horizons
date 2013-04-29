py-NASA-horizons
================

A pure python3 wrapper for JPL HORIZONS on-line solar system data and ephemeris computation service.
It uses the telnet interface.

current strategy: set up a context to query (object and daterange) and
retrieve data from it.

TODO:

* handle telnet errors
* refactor date handling

references
==========

* [NASA HORIZONS page](http://ssd.jpl.nasa.gov/?horizons)
* [ISO 8601](http://de.wikipedia.org/wiki/ISO_8601)
* [RFC 854 - telnet](http://tools.ietf.org/html/rfc854.html)
* [RFC 4180 - CSV](http://tools.ietf.org/html/rfc4180.html)
* [RFC 4627 - JSON](http://tools.ietf.org/html/rfc4627) and [json.org](http://json.org/)
* [YAML specification](http://yaml.org/spec/)
* [PyYAML](https://bitbucket.org/xi/pyyaml)
* [United States Naval Observatory Circular 179 : The IAU Resolutions on Astronomical Reference Systems, Time Scales, and Earth Rotation Models Explanation and Implementation (pdf)](http://aa.usno.navy.mil/publications/docs/Circular_179.pdf)
* [pytest testing framework](http://www.pytest.org)