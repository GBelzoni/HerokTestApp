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
file = open('GraphAPIQueries/fetch_feed_ids.txt')
get_qry = file.read()
file.close()

#get unix time for x time ago.
import datetime
import time
minutes_offset = 0
now = datetime.datetime.now()
td = datetime.timedelta(minutes = minutes_offset)
since_dt = now-td
since_unixtime = time.mktime(since_dt.timetuple())

import webbrowser
get_qry
page = 'KTNKenya'

posts_backto_offset = datetime.timedelta(hours = 24)
posts_since = now - posts_backto_offset
posts_since_unix = int(time.mktime(posts_since.timetuple()))
posts_since
posts_since_unix

comments_backto_offset = datetime.timedelta( minutes = minutes_offset)
comments_since = now - comments_backto_offset
comments_since
comments_since_unix = int(time.mktime(comments_since.timetuple()))
comments_since_unix

(comments_since_unix - posts_since_unix)/60.0

get_qry
get_qry2 = 'https://'+get_qry.format(page,
                                     posts_since_unix,
                                     comments_since_unix,
                                     longAT)
comments_since_unix
print get_qry2

#webbrowser.open_new_tab(get_qry2)

#Do FB Graph API GET request
r = requests.get(get_qry2)
r.status_code
r.text
jdata = r.json()
jdata
ids = [ it['id'] for it in jdata['feed']['data']]
ids

file = open('GraphAPIQueries/fetch_feed_data3.txt')
get_qry_data = file.read()
file.close()

get_qry_data2 = 'https://'+get_qry_data.format(ids[1],longAT)
get_qry_data2


for it in ids[0:3]:
    get_qry_data2 = 'https://'+get_qry_data.format(it,longAT)
    r2 = requests.get(get_qry_data2)
    rdata2 = r2.json()
    try:
        print len(rdata2['comments']['data'])
        print rdata2['comments']['data']
    except:
        print 'no comments for {}'.format(rdata2['id'])
        continue
    
    
