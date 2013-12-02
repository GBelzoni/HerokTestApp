import os
os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')
from DBmanagement import *
from fb_query import *

import fb_query
reload(fb_query)


#Setup fbquery object
fb1 = fb_query.fb_query(start_upd_offset = datetime.timedelta(hours=24))
fb1.access_token

#Set up test page to query
page_info = { 'url' : 'KTNKenya',
              'page_name' : 'KTNKenya' }

#Do query
fb1.do_id_query(page_info)
fb1.post_ids
fb1.do_comments_query()

fb1.query_results[0]
fb1.to_records() #Convert to records


#Get Source List
import pandas as pd
df = pd.read_csv('UmatiSources.csv')
df = df.ix[0:10]
Names = df['Name of Site/Page'].values.tolist()
Names
df
URLs = df['URL'].values.tolist()
URLs
len(URLs)

page_infos = zip(Names,URLs)
page_infos = [ {'page_name' : it[0], 'url' : it[1]} for it in page_infos]


i=0
for it in page_infos:
    try:
        fb1.do_id_query(it)
        print 'success for {0}, row {1}'.format(it['page_name'],i)
    except:
        print 'Error for {0}, row {1}'.format(it['page_name'],i)
        

print status
if status != 400:
    print len(fb1.to_records())
page_infos[6]
fb1.to_json()


num = 10
page_infos[num]
#query fb data
record_list = get_latest_posts(page_infos[num]) 
len(record_list)
#Add to db
record_list[0]
session = setup_sqlalchemy()
for rc in record_list:
    add_record(rc,session)


