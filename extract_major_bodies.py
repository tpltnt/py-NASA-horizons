#!/usr/bin/env python3
import datetime
import json
import socket
import telnetlib

"""a simple script to extract major body object information
from NASA HORIZON."""

host    = "horizons.jpl.nasa.gov"
port    = 6775
timeout = 9999
telnetsession = None

try:
    telnetsession = telnetlib.Telnet(host, port, timeout)
except socket.timeout:
    raise IOError("socket timed out")

telnetsession.read_until(b"Horizons> ")
telnetstring = "MB".encode('ascii')
telnetsession.write(telnetstring + b"\n")
# major bodies
sessioncontent = telnetsession.read_until(b"Use ID# to make unique selection.")
# chunk the session content into lines again
datalines = str(sessioncontent).split("\\r\\n")
# delete crust
for i in range(0,6):
    del datalines[0]
del datalines[-2]
# extract number of records
counter = datalines[-1]
counter = counter.split("=")[1].strip()
counter = counter.split(".")[0]
counter = int(counter)
# delete last line (contained counter)
del datalines[-1]
# check for full retrieval
if len(datalines) < counter:
    raise IOError("too few datapoints received")
if len(datalines) > counter:
    raise IOError("received more datapoints than expected")


# close session
telnetsession.write(b"exit\n")
telnetsession.close()
