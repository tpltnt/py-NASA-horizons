#!/usr/bin/env python3
import yaml
import socket
import telnetlib

"""a simple script to extract major body object information
from NASA HORIZON and create a reST table/cheatsheet."""

host    = "horizons.jpl.nasa.gov"
port    = 6775
timeout = 9999
telnetsession = None
headings = ["ID number", "designation","IAU/other"] # for final table

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
telnetsession.write(b"quit\n")
telnetsession.close()

# parse data into list of dictionaries
allobjects = []
for line in datalines:
    # [{},{}]
    idnumber = int(line[0:9].strip())
    name = line[11:45].strip()
    if "" == name:
        name = None
    designation = line[46:57].strip()
    if "" == designation:
        designation = None
    other = line[59:80].strip()
    if "" == other:
        other = None
    dataset = dict(idnumber=idnumber,
                   designation=designation,
                   other=other)
    allobjects.append(dataset)

# create rst-file with table
## determine max cell width
maxid = 0
maxdes = 0
maxother = 0
for dataset in allobjects:
    if maxid < len(str(dataset['idnumber'])):
        maxid = len(str(dataset['idnumber']))
    if maxdes < len(str(dataset['designation'])):
        maxdes = len(str(dataset['designation']))
    if maxother < len(str(dataset['other'])):
        maxother = len(str(dataset['other']))
### also take heading into account
if maxid < len(headings[0]):
    maxid = len(headings[0])
if maxdes < len(headings[1]):
    maxdes = len(headings[1])
if maxother < len(headings[2]):
    maxother = len(headings[2])

## flush out the data
rstfile = open('major_body_sheet.rst','w')

### create heading
#### top line
rstfile.write("+")
for i in range(maxid+2):
    rstfile.write("-")
rstfile.write("+")
for i in range(maxdes+2):
    rstfile.write("-")
rstfile.write("+")
for i in range(maxother+2):
    rstfile.write("-")
rstfile.write("+\n")
#### text
rstfile.write("| ")
rstfile.write(headings[0])
for i in range(maxid - len(headings[0])):
    rstfile.write(" ")
rstfile.write(" | ")
rstfile.write(headings[1])
for i in range(maxdes - len(headings[1])):
    rstfile.write(" ")
rstfile.write(" | ")
rstfile.write(headings[2])
for i in range(maxother - len(headings[2])):
    rstfile.write(" ")
rstfile.write(" |\n")
#### bottom line
rstfile.write("+")
for i in range(maxid+2):
    rstfile.write("=")
rstfile.write("+")
for i in range(maxdes+2):
    rstfile.write("=")
rstfile.write("+")
for i in range(maxother+2):
    rstfile.write("=")
rstfile.write("+\n")

rstfile.close()
