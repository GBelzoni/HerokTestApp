import json

f= open('test_KTNews_data')
result = f.read()
f.close()

result_dict = json.loads(result)
result_dict['posts']['data']
#first layer - posts
result_dict['posts']['data'][0].keys()

#second layer - comments on post
result_dict['posts']['data'][0]['comments']['data'][0]
result_dict['posts']['data'][0]['comments']['paging']
