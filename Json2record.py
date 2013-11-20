import os
import json

os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')

columns = ['id', 'posts.data.message', 'posts.data.id', 'posts.data.created_time', 'posts.data.comments.data.id', 'posts.data.comments.data.message','posts.data.comments.data.from.name','posts.data.comments.data.from.id','posts.data.comments.data.created_time']

txt_columns = ','.join(columns) +'\n'

f=open('test_KTNews_data.json')
jdata = json.loads(f.read())
f.close()

l1 = ['a','b']
l2 = list(l1)
l2 += [1]
l1

fout.close()
fout = open( 'test_query.csv','w')
fout.write(txt_columns)
jdata['id'] 
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

jdata['posts']['data'][0]['message'].encode('utf-8')


