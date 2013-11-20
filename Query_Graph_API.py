import requests
import os

os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')

App_ID='714612301882745'
App_Secret="439aa3a5e9e0143928984cdb33d55176"

file_AT = open('long_AT.txt')
longAT =file_AT.read()
file_AT.close()

file = open('GraphAPIQueries/test_single_fetch_posts.txt')
get_qry = file.read()
file.close()
get_qry
get_qry2 = 'https://'+get_qry.format(longAT)
get_qry2
r = requests.get(get_qry2)
r.status_code


# Still working on this
j_data = r.json()
j_data

import pandas.io.json as pjson
pjson.json_normalize(j_data).to_csv('text_pdjsn.csv')

j_data2 = open('test_KTNews_data').read()
j_data2 = '[' + j_data2 + ']'
j_data2 = json.loads(j_data2)
j_data2
pjson.json_normalize(j_data,['posts',['data']] )
import



import pandas as pd
pd.read_json('test_KTNews_data',orient='columns')
import json
fout = open('test_KTNews_data.txt','w')
fout.write(r.text)
fout.close()
