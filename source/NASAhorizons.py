#!/usr/bin/env python3
"""
A pure python 3 wrapper for the `NASA HORIZONS <http://ssd.jpl.nasa.gov/?horizons>`_
data service.

.. moduleauthor:: tpltnt
"""

import datetime
import json
import socket
import telnetlib


class NASAhorizons(object):
    """
    A python wrapper for the `NASA HORIZONS <http://ssd.jpl.nasa.gov/?horizons>`_ 
    data service telnet interface to query xyz-coordinates of objects.
    It uses the ICRF/J2000.0 reference frame.
    """

    __referenceframe = "J2000"
    __objectid = None       # horizon interal object id to query
    __telnetsession = None

    def __init__(self):
        self.create_session()

    def create_session(self):
        """
        Creates a new telnet connection to the NASA HORIZONS data service.
        Calling this method *will destroy* your old connection.

        :raises: IOError

        """

        host = "horizons.jpl.nasa.gov"
        port = 6775
        timeout = 120

        try:
            self.__telnetsession = telnetlib.Telnet(host, port, timeout)
        except socket.timeout:
            raise IOError("socket timed out")

    def has_session(self):
        """
        A simple self test if a session already exits.

        :returns: bool

        >>> nasa = NASAhorizons()
        >>> nasa.create_session()
        >>> nasa.has_session()
        True
        """
        if None == self.__telnetsession:
            return False
        else:
            return True

    def close_session(self):
        """
        Explictly close the session.
        """
        self.__telnetsession.write(b"exit\n")
        self.__telnetsession.close()
        self.__telnetsession = None

    def set_object_id(self, idnumber):
        """
        Select object by its HORIZONS internal ID number.
        Note that these are *not* the IAU or designation numbers.
        Negative values indicate spacecrafts.

        :param idnumber: HORIZONS-internal ID number, see :doc:`major_body_sheet`
        :type idnumber: int
        :raises: TypeError
        """
        if not isinstance(idnumber, int):
            raise TypeError("ID numbers need to be integers.")
        self.__objectid = idnumber

    def convert_to_NASA_date(self, dateobject):
        """
        Convert a given datetime.date-object to a string in NASA format.

        :param dateobject: date to convert
        :type dateobject: datetime.date
        :returns: str -- date in NASA format
        :raises: TypeError

        >>> import datetime
        >>> test = datetime.date(year=1977, month=9, day=10)
        >>> convert_to_NASA_date(test)
        1977-Sep-10

        .. todo::

        * refactor date handling (datetime.date is insufficient)
        """
        if not isinstance(dateobject, datetime.date):
            raise TypeError("given date has to be datetime.date-object")

        # convert year
        datestring = str(dateobject.year) + "-"

        # crude cascade conversion for month
        if 1 == dateobject.month:
            datestring += "Jan-"
        if 2 == dateobject.month:
            datestring += "Feb-"
        if 3 == dateobject.month:
            datestring += "Mar-"
        if 4 == dateobject.month:
            datestring += "Apr-"
        if 5 == dateobject.month:
            datestring += "May-"
        if 6 == dateobject.month:
            datestring += "Jun-"
        if 7 == dateobject.month:
            datestring += "Jul-"
        if 8 == dateobject.month:
            datestring += "Aug-"
        if 9 == dateobject.month:
            datestring += "Sep-"
        if 10 == dateobject.month:
            datestring += "Oct-"
        if 11 == dateobject.month:
            datestring += "Nov-"
        if 12 == dateobject.month:
            datestring += "Dez-"

        # convert day
        datestring += str(dateobject.day)

        return datestring

    def convert_NASA_to_ISO_datestring(self, nasadate):
        """
        Convert a NASA string to an `ISO 8601 <http://de.wikipedia.org/wiki/ISO_8601>`_
        like format. The time is in
        `Barycentric Dynamical Time <http://en.wikipedia.org/wiki/Barycentric_Dynamical_Time>`_.

        :param nasadate: NASA date string
        :type nasadate: str
        :returns: str in ISO-like format
        :raises: TypeError

        >>> convert_NASA_to_ISO_datestring("A.D. 1977-Sep-10 00:00:00.0000")
        1977-09-10T00:00:00.0000
        >>> convert_NASA_to_ISO_datestring("B.C. 1977-Sep-10 23:10:00.0000")
        -1977-09-10T23:10:00.0000
        """

        if not isinstance(nasadate, str):
            raise TypeError("i want to eat strings, nothing else ... nom nom nom")
        # AD vs BC
        datechunk = nasadate.replace("A.D. ", "")
        datechunk = datechunk.replace("B.C. ", "-")
        # crude reverse month cascade
        datechunk = datechunk.replace("Jan", "01")
        datechunk = datechunk.replace("Feb", "02")
        datechunk = datechunk.replace("Mar", "03")
        datechunk = datechunk.replace("Apr", "04")
        datechunk = datechunk.replace("May", "05")
        datechunk = datechunk.replace("Jun", "06")
        datechunk = datechunk.replace("Jul", "07")
        datechunk = datechunk.replace("Aug", "08")
        datechunk = datechunk.replace("Sep", "09")
        datechunk = datechunk.replace("Oct", "10")
        datechunk = datechunk.replace("Nov", "11")
        datechunk = datechunk.replace("Dez", "12")
        # split date from time
        datechunk = datechunk.replace(" ", "T")
        return datechunk

    def get_data(self, start, end, format="list"):
        """
        Retrieve data (xyz-coordinates) for formerly selected object.
        A session will be initialized in the background if needed.

        :param start: date of first datapoint to be requested
        :type start: datetime.date
        :param end: date of last datapoint to be requested
        :type end: datetime.date
        :param format: format of returned data
        :type format: str -- "list" (of dictionaires (default)) or "`json <http://json.org/>`_"
        :return: data in selected format
        :raises: Exception, TypeError

        >>> nasa = NASAhorizons()
        >>> nasa.set_object_id(199)
        >>> start = datetime.date(year=1977, month=9, day=10)
        >>> end = datetime.date(year=1977, month=9, day=12)
        >>> nasa.get_data(start, end, format="list")
        [{'z': -0.02967482538878673, 'y': 0.02365967857453419, 'x': 0.3497488933057855, 'date': '1977-09-10T00:00:00.0000'}, {'z': -0.02647449350730847, 'y': 0.05283430192085586, 'x': 0.3408485768468899, 'date': '1977-09-11T00:00:00.0000'}, {'z': -0.02308289285966815, 'y': 0.08159238988582097, 'x': 0.3294953295232826, 'date': '1977-09-12T00:00:00.0000'}]
        """
        # input sanity checks
        if not isinstance(start, datetime.date):
            raise TypeError("start has to be a datetime.date-object")
        if not isinstance(end, datetime.date):
            raise TypeError("end has to be a datetime.date-object")
        if start.year < end.year:
            raise ValueError("start year has to be at least end year")
        if start.month < end.month:
            raise ValueError("start month has to be at least end month")
        if start.day < end.day:
            raise ValueError("start day has to be at least end day")
        # ugly hack to make things work with same date
        __samedayhack = False
        if start == end:
            __samedayhack = True
            end.day += 1
        # end sameday-hack
        if None == self.__objectid:
            raise Exception("no object ID set :( ... please do it next time")
        if not self.has_session():
            self.create_session()
        # telnetstring represent user input (without RET)
        # select object
        self.__telnetsession.read_until(b"Horizons> ")
        telnetstring = str(self.__objectid).encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select [E]phemeris
        self.__telnetsession.read_until(b"<cr>: ")
        telnetstring = "E".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select vectors
        self.__telnetsession.read_until(b"[o,e,v,?] : ")
        telnetstring = "v".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select center-sun
        self.__telnetsession.read_until(b"[ <id>,coord,geo  ] : ")
        telnetstring = "@0".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select reference plane
        self.__telnetsession.read_until(b"[eclip, frame, body ] : ")
        telnetstring = "eclip".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # start date
        self.__telnetsession.read_until(b"] : ")
        telnetstring = self.convert_to_NASA_date(start).encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # end date
        self.__telnetsession.read_until(b"] : ")
        telnetstring = self.convert_to_NASA_date(end).encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select output interval
        self.__telnetsession.read_until(b"] : ")
        telnetstring = "1d".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # change output defaults
        self.__telnetsession.read_until(b"[ cr=(y), n, ?] : ")
        telnetstring = "n".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select output reference frame
        self.__telnetsession.read_until(b"] : ")
        telnetstring = "J2000".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # no light-time corrections
        self.__telnetsession.read_until(b"]  : ")
        telnetstring = "1".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select AU-D as output unit
        self.__telnetsession.read_until(b"] : ")
        telnetstring = "2".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select Spreadsheet CSV format
        self.__telnetsession.read_until(b"] : ")
        telnetstring = "YES".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # Label cartesian output
        self.__telnetsession.read_until(b"] : ")
        telnetstring = "YES".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # select only position components {x,y,z}
        self.__telnetsession.read_until(b"] : ")
        telnetstring = "1".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # read stuff between $$SOE and $$EOE
        self.__telnetsession.read_until(b"$$SOE")
        sessioncontent = self.__telnetsession.read_until(b"$$EOE")
        # chunk the session content into lines again
        datalines = str(sessioncontent).split("\\r\\n")
        # remove $$SOE & $$EOE part
        del datalines[0]
        del datalines[-1]
        data = []
        for line in datalines:
            fields = line.split(",")
            # put all the thing in the data to be returned
            data.append(dict(
                    date = self.convert_NASA_to_ISO_datestring(fields[1].strip()),
                    x = float(fields[2].strip()),
                    y = float(fields[3].strip()),
                    z = float(fields[4].strip())))
        # the same-day hack returns
        if __samedayhack:
            data.pop()
        # finally return data
        if "list" == format:
            return data
        if "json" == format:
            return json.dumps(data)
