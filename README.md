# Open Air

This project is done in the framework of hackita.
It's main aim is to make air quality monitoring data more accessible.
The data in use in this project is the data collected by the 
[Ministry of Environment in Israel](http://www.svivaaqm.net/).


## Development

First, run the initial requirements and local database setup:

```bash
$ mkvirtualenv openair  # Using a Python virtualenv is highly recommended
$ pip install -r requirements.txt
$ python manage.py syncdb --migrate
```

Next, you can import some data using:

```bash
python manage.py hardcode_zones_to_db
python manage.py run_scraper
python manage.py scrape_stations_info
```

You now have a basic environment to work on :)

In order to populate the database again with new records run the command:

```bash
python manage.py run_scraper
```

## Currently available views

Except from the admin panel the following views are available.

home:
``'/'``.

parameter:
``'/parameter/<abbr>/'``.

parameter_json:
``'/parameter/<abbr>/json'``. Returns a json that contains the latest records of the
selected parameter. Used to generate D3 visualizations.

stationmap:
``'/stationmap/<url_id>/'``.

stationmap_json:
``'/stationmap/json/<url_id>/<abbr>/'``. Returns a json that contains the records of the
selected station. Used to generate D3 visualizations.

stationmap_param:
``'/stationmapparam/<url_id>/<abbr>'``.

stationmapwind:
``'/stationmapwind/<url_id>/'``.

stationmap_json:
``'/stationmapparam/json/<url_id>/<abbr>/'``. Returns a json that contains the list of records of the
selected station and parameter. Used to generate D3 visualizations.


## Visualizations

Not finished yet - but we started to pave the yellow brick road to there.
Our goal is to visualize the data using D3.js. For that - we created an api 
using django-tastypie.

As a beginning - run the server and go to: ``http://localhost:8000/api/v0/station/`` 
or ``http://localhost:8000/api/v0/station/<station.id>``
