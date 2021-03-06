py-NASA-horizons
================

A pure python3 wrapper for JPL HORIZONS on-line solar system data and
ephemeris computation service. This module provides an object to interact
with the service for data retrieval and thus abstracts away the official
telnet interface.. The functionality is currently limited to x-y-z
coordinates of major bodies, but can easily be extended.
The sourcecode can be found in the 'source' directory. The 'test' directory
contains pytest-tests and the 'documentation' directory well ... the
documentation.

quickstart
----------

* start coding by including the ```source``` directory into sys.path
    * currently no pip package
* run tests by typing ```py.test```
* (re)build documentation by running ```cd documentation && make html```
* HTML documentation path: documentation/_build/html/index.html


TODO
----

* handle telnet errors
* refactor date handling

references
==========

* [NASA HORIZONS page](http://ssd.jpl.nasa.gov/?horizons)
* [NASA HORIZONS User Manual](http://ssd.jpl.nasa.gov/?horizons_doc)
* [ISO 8601](http://de.wikipedia.org/wiki/ISO_8601)
* [RFC 854 - telnet](http://tools.ietf.org/html/rfc854.html)
* [RFC 4180 - CSV](http://tools.ietf.org/html/rfc4180.html)
* [RFC 4627 - JSON](http://tools.ietf.org/html/rfc4627) and [json.org](http://json.org/)
* [YAML specification](http://yaml.org/spec/)
* [PyYAML](https://bitbucket.org/xi/pyyaml)
* [United States Naval Observatory Circular 179 : The IAU Resolutions on Astronomical Reference Systems, Time Scales, and Earth Rotation Models Explanation and Implementation (pdf)](http://aa.usno.navy.mil/publications/docs/Circular_179.pdf)
* [reStructuredText documentation](http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html)
* [pytest testing framework](http://www.pytest.org)
* [sphinx documentation generator](http://sphinx-doc.org/)