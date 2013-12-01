import os
os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')
from DBmanagement import *
from fb_query import *

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
page_infos[0]
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


