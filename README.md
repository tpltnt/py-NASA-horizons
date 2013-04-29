py-NASA-horizons
================

A pure python3 wrapper for JPL HORIZONS on-line solar system data and ephemeris computation service.
It uses the telnet interface.

current strategy: set up a context to query (object and daterange) and
retrieve data from it.

TODO:

* check convert_to_NASA_date() for completely correct conversation
* create query-context
* handle telnet errors
* expand convert_NASA_to_ISO_date() to work with complete timestamps

references
==========

* [NASA HORIZONS page](http://ssd.jpl.nasa.gov/?horizons)
* [PyYAML](https://bitbucket.org/xi/pyyaml)
* [pytest testing framework](http://www.pytest.org)
* [ISO 8601](http://de.wikipedia.org/wiki/ISO_8601)

standards documents
-------------------
* [RFC 854 - telnet](http://tools.ietf.org/html/rfc854.html)
* [RFC 4180 - CSV](http://tools.ietf.org/html/rfc4180.html)
* [RFC 4627 - JSON](http://tools.ietf.org/html/rfc4627) and [json.org](http://json.org/)
* [YAML specification](http://yaml.org/spec/)
