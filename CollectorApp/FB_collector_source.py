import os
collector_wd = os.path.dirname(os.path.realpath(__file__))
collector_wd = '/home/phcostello/git/HerokTestApp'
os.chdir(collector_wd)
import logging
import datetime
from CollectorApp.DBmanagement import *


##DB management
session, engine = setup_sqlalchemy()
create_all(engine)
import pickle


#Get Source List
import pandas as pd

# #Get latest post time
# post_times = session.query(Comments.post_created_time)
# EAC_offset = datetime.timedelta(hours = 3)
# post_datetimes = [pd.to_datetime(time)[0] + EAC_offset for time in post_times]
# post_datetimes


import CollectorApp.fb_query as fb_query
reload(fb_query)

# max(post_datetimes)
datetime.datetime.now()
end_window_time = datetime.datetime.now()
# window_delta = datetime.datetime.now() - post_datetimes
import time
window_delta = datetime.timedelta(hours =24 )
latest_time = int(time.mktime(end_window_time.timetuple()))

with  open('CollectorApp/latest_time.txt','w') as f:
    f.write(str(latest_time))

#Setup fbquery object

fb1 = fb_query.fb_query(end_upd_window = end_window_time,
                        start_upd_offset = window_delta)
fb1.access_token

df = pd.read_csv('CollectorApp/UmatiSources_firstClean.csv')
df
Names = df['Name of Site/Page'].values.tolist()
URLs = df['FacebookURL'].values.tolist()

page_infos = zip(Names,URLs)
page_infos = [ {'page_name' : it[0], 'url' : it[1]} for it in page_infos]
logging.basicConfig(filename='main.log', filemode='w',level=logging.DEBUG)

top_level_fields = ['feed','posts']

start_time = time.time()
i=0
#KTNKenya is row 44
#Caroling Mutoko is row 23
# for it in page_infos:
#     log_string = "Name: {0} , url: {1}".format(it['page_name'],it['url'])
#     try:
#         fb1.do_id_query(it,top_level_fields)
#         print 'success for id query {0}, row {1}'.format(it['page_name'],i)
#         logging.info( "Success for id query " + log_string +", row {}".format(i))
#         try:
#             fb1.do_comments_query(300)
#             print "Sucess for comment read for page_name {0} row {1}".format(it['page_name'],i) 
#             logging.info( "Sucess for comment read for page_name {0} row {1}".format(it['page_name'],i))
#             record_list = fb1.to_records()
#             print "converted to records"
#             pickle_name = 'PickleJar/Pickle'+it['page_name']+'.pkl'
#             #Pickle download results for testing
#             out_pkl = open(pickle_name,'wb')
#             pickle.dump(record_list,out_pkl)
#             out_pkl.close()
#             for rc in record_list:
#                 add_record(rc,session)
#             try:
#                 session.commit()
#                 print "Success adding records for {}".format(it['url'])
#             except:
#                 print 'error with db commit'
#                 session.rollback()
#             i+=1
#         except:
#             print "Error for comment read or conver to record for page_name {0} row {1}".format(it['page_name'],i) 
#             logging.info( "Error for comment read for page_name {0} row {1}".format(it['page_name'],i))
#             i+=1
#     except:
#         print 'Error for id query {0}, row {1}'.format(it['page_name'],i)
#         logging.warning( "Failure for id query " + log_string +", row {}".format(i))
#         i+=1
# 
# time_taken = time.time() - start_time



# 
# print "Time taken is ", time_taken/60.0, "minutes"
# session.rollback()
# 
# for i in range(0, len(record_list)):
#     print i
#     add_record(record_list[i],session)
# 
# add_record(record_list[3],session)
# len(record_list)
# session.rollback()
# fb1.post_ids
# for i in range(0, len(record_list)):
#     print record_list[i]['post_comments_message']
#     


#Load saved data
pickles = os.listdir('PickleJar')
pickles[1]#KTN Kenya
rcds = pickle.load(open('PickleJar/'+pickles[1]))

i=0
this_time = rcds[0]['post_comments_created_time']

from dateutil import parser
dt = parser.parse(this_time, ignoretz= True)
dt = dt.replace(tzinfo = None)


for pk in pickles:
    fil = open('PickleJar/'+pk)
    rcds = pickle.load(fil)
    fil.close()
    print pk
    for i in range(0, len(rcds)):
        add_record(rcds[i],session)

session.commit()

    
for i in rcds(0, len(rcds)):
    print rcds[i]['post_comments_message']



query = session.query(Comments.page_name)
query = session.query(Comments.page_name).filter_by(page_name = 'Caroline Mutoko')
len(set(query.all()))