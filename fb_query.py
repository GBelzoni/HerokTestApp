import os
import logging
import requests

os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')

#These come from app I have setup
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


def get_latest_posts( page_info ):


    """
    This queries all comments on posts fro give url
    Input: URL of fb group/user
    Output: list of records of data
    """

    page_name = page_info[0]
    page_url = page_info[1].replace('http://www.facebook.com/','')
    get_qry2 = 'https://'+get_qry.format(page_url,longAT)

    #Do FB Graph API GET request
    r = requests.get(get_qry2)
    r.status_code
    

    #Convert to Json - this converts to python dict object
    jdata = r.json()

    #initialise output list
    records = []

    #loop that converts json to flat dictionary records
    #should build a util that uses recursion - more general
    for it1 in jdata['posts']['data']:

      thisRecord = { 'PageName': page_name,
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

    return records
