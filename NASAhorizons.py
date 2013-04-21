#!/usr/bin/env python3
import socket
import telnetlib

class NASAhorizons(object):
    """a python wrapper for the NASA HORIZONS data service telnet interface"""

    __telnetsession = None
    def __init__(self):
        self.create_telnetsession()


    def create_telnetsession(self):
        """Creates a new telnet connection to the NASA HORIZONS data service.
        Calling this method *will destroy* your old connection."""
        
        host    = "horizons.jpl.nasa.gov"
        port    = 6775
        timeout = 9999

        try:
            self.__telnetsession = telnetlib.Telnet(host, port, timeout)
        except socket.timeout:
            raise IOError("socket timed out")


    def has_session(self):
        """A simple self test if a session already exits."""
        if None == self.__telnetsession:
            return False
        else:
            return True

    def close_session(self):
        """Explictly close the session."""
        self.__telnetsession.write(b"exit\n")
        self.__telnetsession.close()
        self.__telnetsession = None


    def set_object_id(self,idnumber):
        """Select object by its HORIZON internal ID number.
        Note that these are *not* the IAU or designation numbers.
        Negative values indicate spacecrafts."""
        # -31 = Voyager I (test object)
        if not isinstance(idnumber,int):
            raise TypeError("ID numbers need to be integers.")
