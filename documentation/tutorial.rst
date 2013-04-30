Tutorial
========

This page provides some examples of using py-NASA-horizon. It can be used
as a tutorial or as a cookbook. To find out the ID of the object you want
to query, please consult the :doc:`major_body_sheet`.


Getting location of an object at a certain date
-----------------------------------------------
To query one just one day, set start and end to the same date.
 
>>> import datetime
>>> from NASAhorizons import NASAhorizons
>>> # query position of Mercury for January 1st 2013
>>> jpl = NASAhorizons()
>>> jpl.set_object_id(199)
>>> qdate = datetime.date(year=1977, month=1, day=1)
>>> print(jpl.get_data(qdate, qdate))
[{'date': '1977-01-01T00:00:00.0000', 'z': 0.01562549439448472, 'x': 0.09117860868439513, 'y': 0.2894764150799116}]
