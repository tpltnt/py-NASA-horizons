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

print(datalines)

# close session
telnetsession.write(b"exit\n")
telnetsession.close()
