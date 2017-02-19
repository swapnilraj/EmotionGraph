import requests
import json
import scrape
import datetime
import fbid


user_id = fbid.search_username("DonaldTrump")

url = "https://graph.facebook.com/v2.5/%s/feed" % (user_id)

print url

user_access = "EAACEdEose0cBABJIbGAJyCYYcLX91vAjTVKaah0IZANHrSCvkwRhfAhwDKuTCl9ZCcJh6uLiN2b4NsQt2L0dUMj0FLClEcirZADVybMjzwipWI6BORtd1ZAkZA1lwrocLywP5sWYuWrJsVwtZAuIRi4xOATFL5h0GMVZA0O1KZCeLT5vRyJ0ZADxYfmB1MN2hotYZD"

querystring = {"access_token":user_access,"debug":"all","format":"json","method":"get","pretty":"0","suppress_http_code":"1"}

headers = {
    'cacheg': "5aeb7a94-d25b-2134-2aaf-31ac7d560055"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
jn = json.loads(response.text)
print jn
messages = jn["data"]

# print messages[0]["message"]

facebookMessages = []

for message in messages:
    try:
        # print message['message']
        time =  str(message['created_time'])
        time = time.replace("T", " ")
        time = time.replace("+0000", "")
        print time
        year = int(time.split(' ')[0].split('-')[0])
        month = int(time.split(' ')[0].split('-')[1])
        day = int(time.split(' ')[0].split('-')[2])
        hour  = int(time.split(' ')[1].split(':')[0])
        minute = int(time.split(' ')[1].split(':')[1])
        second = int(time.split(' ')[1].split(':')[2])
        facebookMessages.append([' ', datetime.datetime(year, month, day, hour, minute, second), message['message']])
    except KeyError: 
        pass  

scrape.analyzer(facebookMessages) 
