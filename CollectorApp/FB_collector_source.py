import logging
import os
os.chdir('/home/phcostello/git/HerokTestApp')
import datetime
from DBmanagement import *


##DB management
session, engine = setup_sqlalchemy()
create_all(engine)

#Get Source List
import pandas as pd

# #Get latest post time
# post_times = session.query(Comments.post_created_time)
# EAC_offset = datetime.timedelta(hours = 3)
# post_datetimes = [pd.to_datetime(time)[0] + EAC_offset for time in post_times]
# post_datetimes


from fb_query import *
import fb_query

# max(post_datetimes)
datetime.datetime.now()
end_window_time = datetime.datetime.now()
# window_delta = datetime.datetime.now() - post_datetimes

window_delta = datetime.timedelta(hours =10 )

import time
latest_time = int(time.mktime(end_window_time.timetuple()))

with  open('latest_time.txt','w') as f:
    f.write(str(latest_time))

#Setup fbquery object

fb1 = fb_query.fb_query(end_upd_window = end_window_time,
                        start_upd_offset = window_delta)
fb1.access_token
# 
# #Set up test page to query
# page_info = { 'url' : 'myuhurukenyatta',
#               'page_name' : 'http://www.facebook.com/groups/sabaotonline2010/' }
# page_info['url'].replace('http://www.facebook.com/','')
# 
# #Do query
# top_level_fields = ['feed','posts']
# fb1.do_id_query(page_info,
#                 top_level_fields,
#                 ret_qry=True)
# 
# 
# fb1.do_comments_query(10)
# fb1.query_results[0]
# fb1.to_records() #Convert to records



df = pd.read_csv('UmatiSources.csv')
Names = df['Name of Site/Page'].values.tolist()
URLs = df['URL'].values.tolist()

page_infos = zip(Names,URLs)
page_infos = [ {'page_name' : it[0], 'url' : it[1]} for it in page_infos]
logging.basicConfig(filename='main.log', filemode='w',level=logging.DEBUG)



 
top_level_fields = ['feed','posts']
i=0
for it in page_infos:
    log_string = "Name: {0} , url: {1}".format(it['page_name'],it['url'])
    try:
        fb1.do_id_query(it,top_level_fields)
        print 'success for id query {0}, row {1}'.format(it['page_name'],i)
        logging.info( "Success for id query " + log_string +", row {}".format(i))
        try:
            fb1.do_comments_query(300)
            print "Sucess for comment read for page_name {0} row {1}".format(it['page_name'],i) 
            logging.info( "Sucess for comment read for page_name {0} row {1}".format(it['page_name'],i))
            record_list = fb1.to_records()
            for rc in record_list:
                add_record(rc,session)
            try:
                session.commit()
            except:
                print 'error with db commit'
                session.rollback()
            print "Success adding records for {}".format(it['url'])
            i+=1
        except:
            print "Error for comment read for page_name {0} row {1}".format(it['page_name'],i) 
            logging.info( "Error for comment read for page_name {0} row {1}".format(it['page_name'],i))
            i+=1
    except:
        print 'Error for id query {0}, row {1}'.format(it['page_name'],i)
        logging.warning( "Failure for id query " + log_string +", row {}".format(i))
        i+=1



