#Contruct query with correct times
import requests

s1 = 'graph.facebook.com/KTNKenya?fields=posts.fields(message,comments.fields(created_time)'


#These come from app I have setup
App_ID='714612301882745'
App_Secret="439aa3a5e9e0143928984cdb33d55176"

#Read Access token
file_AT = open('long_AT.txt')
longAT =file_AT.read()
longAT = longAT.strip()
file_AT.close()

#Read query for getting data
file = open('GraphAPIQueries/fetch_feed_data.txt')
get_qry = file.read()
file.close()

#get unix time for x time ago.
import datetime
import time
minutes_offset = 60
now = datetime.datetime.now()
td = datetime.timedelta(minutes = minutes_offset)
since_dt = now-td
since_unixtime = time.mktime(since_dt.timetuple())
since_unixtime

get_qry2


get_qry
page = 'KTNKenya'
get_qry2 = 'https://'+get_qry.format(page,longAT,since_unixtime)
get_qry2


#Do FB Graph API GET request
r = requests.get(get_qry2)
r.status_code
r.text
