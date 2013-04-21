#!/usr/bin/env python3

class NASAhorizons(object):
    """a python wrapper for the NASA HORIZONS data service telnet interface"""
    import telnetlib

    __telnetsession = None
    def __init__(self):
        print("foo")

    def create_telnetsession(self):
        """Creates a new telnet connection to the NASA HORIZONS data service.
        Calling this method *will destroy* your old connection."""
        host    = "horizons.jpl.nasa.gov"
        port    = 6775
        timeout = 9999

        try:
            self.__telnetsession = telnetlib.Telnet(host, port, timeout)
        except socket.timeout:
            raise Exception("socket timed out")
