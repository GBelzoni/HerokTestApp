import requests


query_str = 'KTNKenya?fields=posts.fields(message,comments.fields(message))'
query_str2 = 'KTNKenya?'

auth_key = 'CAACEdEose0cBALMZALXlbUFEnXGmvj5Ijs4jjdTZBdavF2czc3vtlgAz4eQ0zAVuNbbZA7NzhTCjAV1mieBQMOaWzFYOjwNkd737Slg3OnKws9nW4ZCpyDvXcVWZCwHi0LAwpueLbpZCirOOfCZBTZBmFW3KiSa08VD89sg2XpD4cDkN9l34t7R7Bi7pqno80RVuBMVc1z0ohgZDZD'

graph_url = 'https://graph.facebook.com/'

get_str = graph_url + query_str + '&access_token=' + auth_key


print get_str



r =requests.get(get_str)
r.text

