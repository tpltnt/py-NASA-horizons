#!/usr/bin/env python3
import datetime
import json
import socket
import telnetlib

class NASAhorizons(object):
    """a python wrapper for the NASA HORIZONS data service telnet interface"""

    __objectid = None       # horizon interal object id to query
    __telnetsession = None
    def __init__(self):
        self.create_session()


    def create_session(self):
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
        if -31 != idnumber:
            raise NotImplementedError("sorry, did not found the time to implement that")
        self.__objectid = idnumber


    def convert_to_NASA_date(self, dateobject):
        """convert given datetime.date-object to string in NASA format,
        e.g. 1977-Sep-10
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
        if 1 == dateobject.month:
            datestring += "Jan-"
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


    def get_data(self,start,end):
        """retrieve data from pre-defined context.
        Right know fixed to Voyager I.

        arguments:
        * start: datetime.date indicating first datapoint to be requested
        * end: datetime.date indicating last datapoint to be requested
        """
        # TODO: check for data context
        if not isinstance(start,datetime.date):
            raise TypeError("start has to be a datetime.date-object")
        if not isinstance(end,datetime.date):
            raise TypeError("end has to be a datetime.date-object")
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
        ####--------------------------------------------######
        telnetstring = "1977-Sep-07".encode('ascii')
        self.__telnetsession.write(telnetstring + b"\n")
        # end date
        self.__telnetsession.read_until(b"] : ")
        telnetstring = "1977-Sep-10".encode('ascii')
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
        print(datalines)
        data = []
        for line in datalines:
            fields = line.split(",")
            # put all the thing in the data to be returned
            data.append(dict(
                    date = fields[1].strip(),
                    x = float(fields[2].strip()),
                    y = float(fields[3].strip()),
                    z = float(fields[4].strip())
                    ))
        # fake test data
        # data = [{'x': 23}, {'y': 42}]
        return json.dumps(data)

# only call if script is executed (and not included) for debugging
if __name__ == '__main__':
    foo = NASAhorizons()
    foo.set_object_id(-31)
    start = datetime.date(year=1977, month=9, day=10)
    end = datetime.date(year=1977, month=9, day=20)
    print(foo.get_data(start, end))
