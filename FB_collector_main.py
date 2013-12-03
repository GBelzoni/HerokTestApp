import logging
import os
os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')
from DBmanagement import *
##DB management
session, engine = setup_sqlalchemy()
create_all(engine)


#Get Source List
import pandas as pd

#Get latest post time
post_times = session.query(Comments.post_created_time)
EAC_offset = datetime.timedelta(hours = 3)
post_datetimes = [pd.to_datetime(time)[0] + EAC_offset for time in post_times]
post_datetimes


from fb_query import *
import fb_query
reload(fb_query)
max(post_datetimes)
datetime.datetime.now()
end_window_time = datetime.datetime.now()
window_delta = datetime.datetime.now() - max(post_datetimes)

import time
int(time.mktime(end_window_time.timetuple()))


#Setup fbquery object
fb1 = fb_query.fb_query(end_upd_window = end_window_time,
                        start_upd_offset = window_delta)
fb1.access_token

#Set up test page to query
page_info = { 'url' : 'http://www.facebook.com/239616172813899',
              'page_name' : 'http://www.facebook.com/groups/sabaotonline2010/' }

page_info['url'].replace('http://www.facebook.com/','')

#Do query
#fb1.do_id_query(page_infos[20],ret_qry=True)
#fb1.post_ids
#fb1.do_comments_query()
#fb1.query_results[0]
#fb1.to_records() #Convert to records



df = pd.read_csv('UmatiSources.csv')
#df = df.ix[0:10]
Names = df['Name of Site/Page'].values.tolist()
Names
df
URLs = df['URL'].values.tolist()
URLs
len(URLs)

page_infos = zip(Names,URLs)
page_infos = [ {'page_name' : it[0], 'url' : it[1]} for it in page_infos]

logging.basicConfig(filename='main.log', filemode='w',level=logging.DEBUG)



 

i=0
for it in page_infos[20:21]:
    log_string = "Name: {0} , url: {1}".format(it['page_name'],it['url'])
    try:
        fb1.do_id_query(it)
        print 'success for id query {0}, row {1}'.format(it['page_name'],i)
        logging.info( "Success for id query " + log_string +", row {}".format(i))
        try:
            fb1.do_comments_query()
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

record_list
session.rollback()



num = 10
page_infos[num]
#query fb data
record_list = get_latest_posts(page_infos[num]) 
len(record_list)
#Add to db
record_list[0]




