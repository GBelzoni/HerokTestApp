import requests

App_ID='714612301882745'
App_Secret="439aa3a5e9e0143928984cdb33d55176"
AT = "CAAKJ76Rn5XkBAH5IaavZB1c8e8ePLYR3Etj34tRIo4SDcHrqSKTb0e9bZAXLZBPLDVCR8IYUyQBFfMh5oHf2FXwOvzTdWIbW8LlniNwgNnRP56XpdqkXVNPcKNY81ZA6XUyP4tWRqjD36MdiSNLBaOzhbYwrcYAyn3fWKeUZCpy41idR9BClOIglZB7sv4BoMgrvHiJdQ15wZDZD"


grapfburl = 'https://graph.facebook.com'

get_qry1 ='/oauth/access_token?grant_type=fb_exchange_token'
get_qry2 = '&client_id={0}&client_secret={1}&fb_exchange_token={2}'.format(App_ID,App_Secret,AT)

get_qry = grapfburl + get_qry1 + get_qry2
r = requests.get(get_qry)
r.status_code

str_with_token = r.text
print str_with_token
f = open('long_AT.txt','w')
token = str_with_token.split('=')
token = token[1]
token = token.split('&')[0]
f.write(token)
f.close()
