'''
Scraper for http://www.svivaaqm.net/

Run standalone as:
python scraper.py [zone|station] <url_id>

Functions
---------
scrape_station(url_id) -> records
scrape_zone(url_id) -> records

Notes
-----
- The parameters as obtained from scrape_station have different
abbreviations then those obtained by scrape_zone. Be sure to select
one set of abbreviations to work with in advance!
- In the records returned from the function scrape_zone there is also
timestamp information, named 'timestamp', as one of the parameters of
each station. Timestamp values are strings.
'''

import sys
import urllib2
from bs4 import BeautifulSoup


def minus_move(value):
    '''
    Check if there is a minus at the end of the string. If so move
    it to the beginning and cast to float (right-to-left problem).

    '''

    try:
        if value[-1] == '-':
            value = float('-{}'.format(value[:-1]))
    except Exception, e:
        pass    

    return value


def scrape_station(url_id):
    '''
    Scrap air parameters from
    http://www.svivaaqm.net/Online.aspx?ST_ID=<STATION_ID>;0

    Parameters
    ----------
    url_id : int
        Replaces <STATION_ID> in the url.

    Returns
    -------
    records : dict
        Dictionary of abbr:value pairs. Abbrevations are strings
        and values are floats.
    '''

    url ='http://www.svivaaqm.net/Online.aspx?ST_ID={};0' \
        .format(url_id)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    soup = BeautifulSoup(response.read())
    table = soup.find('table',
                       border='1',
                       bordercolor='navy',
                       cellpadding='0',
                       cellspacing='0')

    records = {}
    # the first two rows in the table are for heading
    for element in table.find_all('tr')[2:]:
        abbr = str(element.a.string.split('[')[0])
        try:  # to cast to float
            value = float(element.b.string)
        except (ValueError):
            value = None

        records[abbr] = value

    return records


def scrape_zone(url_id):
    '''
    Scrap air parameters from
    http://www.svivaaqm.net/DynamicTable.aspx?G_ID=<ZONE_ID>

    Parameters
    ----------
    url_id : int
        Replaces <ZONE_ID> in the url.

    Returns
    -------
    records : dict
        Dictionary of station:dict pairs. Stations are the url_id
        of the station and the dict are the records as received by
        scrape_station() function (see module notes).
    '''

    url ='http://www.svivaaqm.net/DynamicTable.aspx?G_ID={}' \
        .format(url_id)

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(url)
    soup = BeautifulSoup(response.read())
    table = soup.find('table',
                       id='C1WebGrid1')

    # the first row in the table is for abbreviations
    abbreviations = ['timestamp']
    # the relevant cells are located in positions 3 to -1
    for cell in list(table.find('tr'))[3:-1]:
        abbr = str(cell.div.get_text().strip('\r\n\t'))
        abbreviations.append(abbr)

    # start scrape parameter values
    records = {}
    for element in table.find_all('tr')[2:]:

        # station url_id can be found in a the link
        # in the beginning of each row
        station_url_id = int(element.a.get('href').split('=')[1])
        station_records = {}

        for i, cell in enumerate(list(element.find_all('td'))[1:]):

            value = cell.div.get_text().strip('\r\n\t')

            try:  # to cast to float
                value = float(value)
            except ValueError:
                try:  # to cast to string
                    value = str(value)
                except UnicodeEncodeError:
                    value = None

            value = minus_move(value)

            station_records[abbreviations[i]] = value

        records[station_url_id] = station_records

    return records


def print_station_records(records):
    for k in records.keys():
        print('{0:18}\t{1}'.format(k, records[k]))


def print_zone_records(records):
    for station_url_id in records.keys():
        text = 'Scraping station {}'.format(station_url_id)
        print(text)
        print('-' * len(text))
        print_station_records(records[station_url_id])
        print('')  # new line


def main():

    if len(sys.argv) == 3:

        method = sys.argv[1]
        url_id = int(sys.argv[2])

        if method == 'station':
            print('Scraping station {}\n'.format(url_id))
            print_station_records(scrape_station(url_id))
            return

        if method == 'zone':
            print('Scraping zone {}\n'.format(url_id))
            print_zone_records(scrape_zone(url_id))
            return

    print('Type "station" or "zone" and url_id. For example:\n'
              'python scrape.py zone 8')


if __name__ == '__main__':
    main()
