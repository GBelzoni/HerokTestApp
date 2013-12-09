from dateutil import parser
import datetime

def setup_sqlalchemy():
    
    #Define db model
    db_name = 'Collector.sqlite'
    #Create connection to db
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///'+db_name,echo=False)
    
    #connect to engine
    #This next would go where the engine statement is in prod. It is handle to db
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session() #The session object is now the handle to our db

    

    return session, engine
    
#Import columns and types to make table
from sqlalchemy import Column, Integer, String, DateTime

#import base class to make table from
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


#Add records to db
from sqlalchemy.exc import IntegrityError
    
#Define class that represents Comments table
class Comments(Base):
  __tablename__ = 'comments'

  #Define schema
  #id = Column(Integer, primary_key=True)
  page_name = Column(String)
  page_id = Column(Integer)
  post_message = Column(String)
  post_id = Column(Integer)
  post_created_time = Column(DateTime)
  post_comments_id = Column(String, primary_key=True)
  post_comments_message = Column(String)
  post_comments_from_name = Column(String)
  post_comments_from_id = Column(String)
  post_comments_created_time = Column(DateTime) #Column(DateTime(timezone=True))

  #Define
  def __init__(self, record):

    """
    Be nice to find a quicker way to do
    """


    self.page_name = record['PageName']
    self.page_id = record['PageId']
    self.post_message = record['post_message']
    self.post_id = record['post_id']
    self.post_created_time = parser.parse(record['post_created_time'],ignoretz=True)
    self.post_comments_id = record['post_comments_id']
    self.post_comments_message = record['post_comments_message']
    self.post_comments_from_name = record['post_comments_from_name']
    self.post_comments_from_id = record['post_comments_from_id']
    self.post_comments_created_time = parser.parse(record['post_comments_created_time'],ignoretz=True)

     

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


def create_all(engine):
    #Create the tables in db specified by engine
    Base.metadata.create_all(engine)


def add_record(rc,session):
    rc_comments = Comments(rc)
    session.merge(rc_comments) #use merge rather than add to deal with duplicates




