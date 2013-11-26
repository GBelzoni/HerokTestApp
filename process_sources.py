import os
os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')
fin = open('UmatiSources.csv')
text = fin.readlines()
fin.close()
text
text[0]

#Get Source List
import pandas as pd
df = pd.read_csv('UmatiSources.csv')
df = df.ix[0:5]
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
page = URLs[0]
page = 'KTNKenya'
page = page.replace('http://www.facebook.com/','')
get_qry2 = 'https://'+get_qry.format(page,longAT)
get_qry2

#Do lookup
r = requests.get(get_qry2)
r.status_code
print r.text[0:500]

#Convert to Json - this converts to python dict object
jdata = r.json()
jdata.keys()

#Convert to list of records to add
import logging
logging.basicConfig(filename='FBimports.log',level=logging.DEBUG)

records = []
i=0

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


jdata['id']
  
NL = " " #replacement character for new lines
for it1 in jdata['posts']['data']:
  

  #Check if top level post is ok
  try:
    thisRecord['post_message'] = it1['message']
    thisRecord['post_id'] = it1['id']
    thisRecord['post_created_time'] = it1['created_time']]
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

            records.append(row2)
            
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

records

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
  id = Column(Integer, primary_key=True)
  page_id = Column(Integer)
  posts_data_message = Column(String)
  posts_data_id = Column(Integer)
  posts_data_created_time = Column(String)
  posts_data_comments_data_id = Column(Integer)
  posts_data_comments_data_message = Column(String)
  posts_data_comments_data_from_name = Column(String)
  posts_data_comments_data_from_id = Column(Integer)
  posts_data_comments_data_created_time = Column(String)

  #Define
  def __init__(self, record):

    """
    Not the best def in the world as needs data to be in correct ord
    should probably change so records are dictionary
    """
    
    self.page_id = record[0]
    self.posts_data_message = record[1]
    self.posts_data_id = record[2]
    self.posts_data_created_time = record[3]
    self.posts_data_comments_data_id = record[4]
    self.posts_data_comments_data_message = record[5]
    self.posts_data_comments_data_from_name = record[6]
    self.posts_data_comments_data_from_id = record[7]
    self.posts_data_comments_data_created_time = record[8]

     

  def __repr__(self):
    return "<comment('%s','%s','%s','%s','%s','%s','%s','%s')>" % ( self.posts_data_message,
                                               self.posts_data_id,
                                               self.posts_data_created_time,
                                               self.posts_data_comments_data_id,
                                               self.posts_data_comments_data_message,
                                               self.posts_data_comments_data_from_name,
                                               self.posts_data_comments_data_from_id,
                                               self.posts_data_comments_data_created_time)



#Check table def
Comments.__table__

#Create the tables in db specified by engine
Base.metadata.create_all(engine)

#This next would go where the engine statement is in prod. It is handle to db
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session() #The session object is now the handle to our db

#Add records to db

rc_comments.posts_data_id
rc_comments.posts_data_message
rc_comments.posts_data_comments_data_message


for rc in records:
  rc_comments = Comments(rc)
  session.add(rc_comments)

session.commit()


this_comment = session.query(Comments).first()
this_comment
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


