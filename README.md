# open Air
This project is done in the framework of hackita.
It's main aim is to make air quality monitoring data more accessible.
The data in use in this project is the data collected by the ministry of environment in Israel (http://www.svivaaqm.net/).

## Requirements:
Check requirements.txt

## Develping 
Please read HACKING

## For visualization:
Not finished yet - but the we started to pave the yellow brick road to there.
Our goal is to visualize the data using D3.js. For that - we created an api using django-tastypie.
As a beginning - run the server and go to:
http://localhost:8000/api/v0/station/
Check also:
http://localhost:8000/api/v0/station/[station.id]