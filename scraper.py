import sys
import urllib2
from bs4 import BeautifulSoup

def scrap(url_id):
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

    # the first two rows in the table are for heading
    records = {}
    for element in table.find_all('tr')[2:]:
        abbr = element.a.string.split('[')[0]
        try:
            value = float(element.b.string)
        except (ValueError):
            value = None

        records[abbr] = value

    return records


if __name__ == '__main__':
    if len(sys.argv) > 0:
        url_id = sys.argv[1]
    else:
        url_id = 11  # just for example
    print('Showing records for station with url_id = {}' \
        .format(url_id))
    results = scrap(url_id)
    for abbr in results.keys():
        print('{}: {}'.format(abbr, results[abbr]))
