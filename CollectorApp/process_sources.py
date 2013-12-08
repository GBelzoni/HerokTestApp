import os
os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')

#Get Source List
import pandas as pd
df = pd.read_csv('UmatiSources.csv')
df = df.ix[0:10]
Names = df['Name of Site/Page'].values.tolist()
Names
df
URLs = df['URL'].values.tolist()
URLs


#Do request for data
import requests
import os

App_ID='714612301882745'
App_Secret="439aa3a5e9e0143928984cdb33d55176"

#Read Access token
file_AT = open('long_AT.txt')
longAT =file_AT.read()
file_AT.close()

#Read query for getting data
file = open('GraphAPIQueries/fetch_data.text')
get_qry = file.read()
file.close()

#Get URL and create query
URLs[0]
page = 'http://www.facebook.com/pages/Chamgei-FM/150589741636194'
page = 'KTNKenya'
page = URLs[0]
page = 'https://www.facebook.com/239616172813899/'
page = page.replace('https://www.facebook.com/','')
page
get_qry2 = 'https://'+get_qry.format(page,longAT)
get_qry2

#Do lookup
r = requests.get(get_qry2)
r.status_code
print r.text[0:500]

#Convert to Json - this converts to python dict object
jdata = r.json()
jdata.keys()
jdata['id']


#Convert to list of records to add
import logging
logging.basicConfig(filename='FBimports.log',level=logging.DEBUG)


records = []


for it1 in jdata['posts']['data']:

  thisRecord = { 'PageName': page,
               'PageId': jdata['id'],
               'post_message':None,
               'post_id':None,
               'post_created_time':None,
               'post_comments_id':None,
               'post_comments_message':None,
               'post_comments_from_name':None,
               'post_comments_from_id':None,
               'post_comments_created_time':None}
  
  #Check if top level post is ok
  try:
    thisRecord['post_message'] = it1['message']
    thisRecord['post_id'] = it1['id']
    thisRecord['post_created_time'] = it1['created_time']
  except:
    error_str = 'No message in post {}'.format(it1['id'])
    print error_str
    logging.warning(error_str)
    continue #if error then got to next post
  else:
    try:
      for it2 in it1['comments']['data']:
        try:             
            thisRecord['post_comments_id'] = it2['id']
            thisRecord['post_comments_message'] =it2['message']
            thisRecord['post_comments_from_name'] = it2['from']['name']
            thisRecord['post_comments_from_id'] =  it2['from']['id'] 
            thisRecord['post_comments_created_time'] =it2['created_time']
            cp_thisRecord = dict(thisRecord) #Remember to copy dict otherwise only passes ref to dict rather than vals
            records.append(cp_thisRecord)
            
        except:
          error_str = 'Problem with comment id {1}, on post id[2]'.format(it1['id'],it2['id'])
          print error_str
          logging.warning(error_str)
          continue #if error then got to next comment in post
    except:
      error_str = 'No comments for post id {0}'.format(it1['id'])
      print error_str
      logging.warning(error_str)
      continue #if error then got to next comment in post



#Define db model
db_name = 'Collector.sqlite'
#Create connection to db
from sqlalchemy import create_engine
engine = create_engine('sqlite:///'+db_name,echo=True)
#import base class to make table from
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()





#Import columns and types to make table
from sqlalchemy import Column, Integer, String
#Define class that represents table
class Comments(Base):
  __tablename__ = 'comments'

  #Define schema
  #id = Column(Integer, primary_key=True)
  page_name = Column(String)
  page_id = Column(Integer)
  post_message = Column(String)
  post_id = Column(Integer)
  post_created_time = Column(String)
  post_comments_id = Column(String, primary_key=True)
  post_comments_message = Column(String)
  post_comments_from_name = Column(String)
  post_comments_from_id = Column(String)
  post_comments_created_time = Column(String)

  #Define
  def __init__(self, record):

    """
    Be nice to find a quicker way to do
    """

    { 'PageName': page,
               'PageId': jdata['id'],
               'post_message':None,
               'post_id':None,
               'post_created_time':None,
               'post_comments_id':None,
               'post_comments_message':None,
               'post_comments_from_name':None,
               'post_comments_from_id':None,
               'post_comments_created_time':None}

    self.page_name = record['PageName']
    self.page_id = record['PageId']
    self.post_message = record['post_message']
    self.post_id = record['post_id']
    self.post_created_time = record['post_created_time']
    self.post_comments_id = record['post_comments_id']
    self.post_comments_message = record['post_comments_message']
    self.post_comments_from_name = record['post_comments_from_name']
    self.post_comments_from_id = record['post_comments_from_id']
    self.post_comments_created_time = record['post_comments_created_time']

     

  def __repr__(self):
    return "<comment('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.page_name,
                                                                   self.page_id,
                                                                   self.post_message,
                                                                   self.post_id,
                                                                   self.post_created_time,
                                                                   self.post_comments_id,
                                                                   self.post_comments_message,
                                                                   self.post_comments_from_name,
                                                                   self.post_comments_from_id,
                                                                   self.post_comments_created_time)



#Check table def
Comments.__table__

#Create the tables in db specified by engine
Base.metadata.create_all(engine)

#This next would go where the engine statement is in prod. It is handle to db
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session() #The session object is now the handle to our db

records[0]
records[1]
rc_comments = Comments(records[0])

#Check all fields are there

print rc_comments.page_name
print rc_comments.page_id
print rc_comments.post_message
print rc_comments.post_id
print rc_comments.post_created_time
print rc_comments.post_comments_id
print rc_comments.post_comments_message
print rc_comments.post_comments_from_name
print rc_comments.post_comments_from_id
print rc_comments.post_comments_created_time

#Add records to db
from sqlalchemy.exc import IntegrityError

for rc in records:
  #have used post_comments_id as PRIMARY_KEY
  #So should throw IntegretyError if posts already exits
  #this means that can skip this and rollback

  rc_comments = Comments(rc)
  session.add(rc_comments)
  try:
    session.commit()
  except IntegrityError:
    print "post id {0} already in db".format(rc_comments.post_id)
    session.rollback()
    continue                                                      





this_query = session.query(Comments).filter_by(post_comments_id='10153535800975533_25245467')
this_query.all()
session

session.dirty
session.new








#Convert to flat csv
fout = open( 'test_query.csv','w')
columns = ['id', 'posts.data.message', 'posts.data.id', 'posts.data.created_time', 'posts.data.comments.data.id', 'posts.data.comments.data.message','posts.data.comments.data.from.name','posts.data.comments.data.from.id','posts.data.comments.data.created_time']
txt_columns = ','.join(columns) +'\n'
fout.write(txt_columns)
i=0

def to_txtf(txt,NL):
  return '"' + txt.replace('\n',NL) + '"'

NL = " " #replacement character for new lines
for it1 in jdata['posts']['data']:
  row = [ jdata['id']]
  row += [ to_txtf(it1['message'],NL), it1['id'], it1['created_time']]
  for it2 in it1['comments']['data']:
    row2 = list(row)
    row2 += [it2['id'],to_txtf(it2['message'],NL), it2['from']['name'], it2['from']['id'], it2['created_time']]
    txt_row = ','.join(row2)+'\n' 
    print i
    fout.write(txt_row.encode('utf-8'))
    i+=1

fout.close()


