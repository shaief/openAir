'''
Scraper for http://www.svivaaqm.net/

Run standalone as:
python scraper.py <url_id>

Functions
---------
scrap_station(url_id) -> records
scrap_zone(url_id) -> records
'''

import sys
import urllib2
from bs4 import BeautifulSoup


def scrap_station(url_id):
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
        abbr = element.a.string.split('[')[0]
        try:
            value = float(element.b.string)
        except (ValueError):
            value = None

        records[abbr] = value

    return records


def scrap_zone(url_id):
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
        scrap_station() function.
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
    abbreviations = []
    for element in table.find('tr'):
        for cell in element:
            try:
                abbreviations.append(cell.get_text().strip('\r\n\t'))
            except Exception, e:
                pass

    # TODO COMPLETE THE PARSER
    # records = {}
    # for element in table.find_all('tr')[2:]:
    #     station_records = {}
    #     abbr = element.a.string.split('[')[0]
    #     try:
    #         value = float(element.b.string)
    #     except (ValueError):
    #         value = None

    #     records[abbr] = value

    # return records


def main():
    if len(sys.argv) > 1:
        url_id = sys.argv[1]
        print('Showing records for station with url_id = {}' \
            .format(url_id))
        results = scrap(url_id)
        for abbr in results.keys():
            print('{}: {}'.format(abbr, results[abbr]))
    else:
        print('Type "station" or "zone" and url_id')


if __name__ == '__main__':
    # main()
    scrap_zone(8)
