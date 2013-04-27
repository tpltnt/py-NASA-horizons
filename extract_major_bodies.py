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
print(sessioncontent)

# close session
telnetsession.write(b"exit\n")
telnetsession.close()
