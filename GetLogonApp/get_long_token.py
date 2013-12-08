def get_long_AT():
    
    import requests

    #pc_Dev ids
    App_ID='714612301882745'
    App_Secret="439aa3a5e9e0143928984cdb33d55176"
    
    #iHub app
    # App_ID='565857103493139'
    # App_Secret="439aa3a5e9e0143928984cdb33d55176"

    with open('short_AT.txt') as f_shortAT:
        short_AT =f_shortAT.read()
    
    grapfburl = 'https://graph.facebook.com'
    get_qry1 ='/oauth/access_token?grant_type=fb_exchange_token'
    get_qry2 = '&client_id={0}&client_secret={1}&fb_exchange_token={2}'.format(App_ID,App_Secret,short_AT)
    
    get_qry = grapfburl + get_qry1 + get_qry2
    # print get_qry
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
    
    return  token

if __name__ == 'main':
    
    get_long_AT()
