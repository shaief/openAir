#! /bin/python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import numpy as np
 
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open('http://www.svivaaqm.net/Online.aspx?ST_ID=11;0')
 
#url ='http://www.svivaaqm.net/Online.aspx?ST_ID=11;0'
page = urllib2.urlopen(response)
print page.read()
soup = BeautifulSoup(page)
print soup
tr = []
tables = soup.findAll("table")
print tables
for tbl in tables:
    rows = soup.findAll("tr")
    for i,row in enumerate(rows):
        cells = row.findAll("td")
        tr.append(cells[0].get_text())
        print tr
             