import os
import logging
import requests
#get unix time for x time ago.
import datetime
import time

os.chdir('/home/phcostello/Documents/Projects/HerokTestApp')

#These come from app I have setup
App_ID='714612301882745'
App_Secret="439aa3a5e9e0143928984cdb33d55176"

#Read Access token
file_AT = open('long_AT.txt')
longAT =file_AT.read()
file_AT.close()

#Read query for getting post ids
file = open('GraphAPIQueries/fetch_feed_ids.txt')
get_post_ids = file.read()
file.close()

#Read query for getting comments from post
file = open('GraphAPIQueries/fetch_feed_data3.txt')
get_query_data = file.read()
file.close()


class fb_query(object):

    """ Class for managing facebook queries """
    
    def __init__(self,
                 end_upd_window = datetime.datetime.now(),
                 start_upd_offset = datetime.timedelta(hours=24) ):

        """ Constructor for query class
        Input:
        end_upd_window - when the posts are gathere too default is now 
        start_upd_offset - how far back to collect posts
        """

        #Query parameters
        self.access_token = longAT
        self.id_query = get_post_ids
        self.data_query = get_query_data
        self.page_info = None

        #ID query results
        self.page_id = None
        self.post_ids = None
        self.query_results = []

        

        #Create posts update window offset from end_upd_window
        self.end_upd_window = end_upd_window
        posts_since = end_upd_window - start_upd_offset
        print posts_since
        self.posts_since_unix = int(time.mktime(posts_since.timetuple()))

        

    def do_id_query(self, page_info):

        self.page_info = page_info
        page_url = page_info['url'].replace('http://www.facebook.com/','')

        #Get page ids
        id_query2 = 'https://'+self.id_query.format(page_url,
                                                    self.posts_since_unix,
                                                    longAT)

        r_id = requests.get(id_query2)
        
        if r_id.status_code != 400:
            ids_json = r_id.json()
            self.page_id = ids_json['id']
            self.post_ids = [ it['id'] for it in ids_json['feed']['data']]
        

        
    def do_comments_query(self):
        """
        Input:
        URL of facebook
        query_str
        access_token

        Output:
        facebook get request in json format
        """

        if len(self.post_ids) != 0:
            #Get comments from post
            for it in self.post_ids[0:3]:
                get_qry_data2 = 'https://'+self.data_query.format(it,longAT)
                #print get_qry_data2
                r_comments = requests.get(get_qry_data2)
                comments_json = r_comments.json()
                try:
                    print len(comments_json['comments']['data'])
                    self.query_results.append(comments_json)
                except:
                    #Add exception handling here
                    print 'no comments for {}'.format(comments_json['id'])
                    continue
        else:
            print "no ids"
        



    def to_records(self):


        """
        This queries all comments on posts fro give url
        Input: URL of fb group/user
        Output: list of records of data
        """

        #initialise output list
        records = []

        #loop that converts json to flat dictionary records
        #should build a util that uses recursion - more general
        page_name = self.page_info['page_name']

        for it1 in self.query_results:

          thisRecord = { 'PageName': page_name,
                       'PageId': self.page_id,
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
