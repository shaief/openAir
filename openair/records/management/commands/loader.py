 # -*- coding: utf-8 -*-
"""
script to load old data from svivaaqm.net

Health Warning :-/ Stinky code ahead of you. Read on your own risk. 
The code is still not documented, does and not comply to pep8, hence 
it stinks. 

It is a work in progress. 


"""
import pandas as pd
import pytz
from openair.settings.base import TIME_ZONE
from openair.records.models import Zone, Station, Parameter, Record

#record, success = Record.objects.get_or_create(
#                        station=station,
#                        parameter=parameter,
#                        value=results[station_url_id][abbr],
#                        timestamp=timestamp
#                    )
# station url_id should be given as cli parameter

# STATION = url_id
STATION = Station.objects.get(url_id=1)


a = pd.read_csv('openair/StationData1.csv', index_col=[20])

for item in in a.columns
    param = getattr(a, item)
    for date, val in nox.iteritems():
        Record.objects.get_or_create(station=station,
                                     parameter=item,
                                     value=val, 
                                     timestamp=date)
