import sys 
import json 
from tweepy import Cursor, API, OAuthHandler
 
if __name__ == '__main__': 
  user = sys.argv[1]

  ACCESS_TOKEN = '381520903-OwPTkjllzq7T9cmeuloBQzUVUBxjjjD3c3YjBB18'
  ACCESS_SECRET = 'lOBE3wrQZWuPvDoiF4vhfhCZB3oiRbFTArdVmf2CZDBqC'
  CONSUMER_KEY = 'KLRKa701PFkAboW9wMhACOa1x'
  CONSUMER_SECRET = 'OlREM6mGWSy7JvBEhjl4mhtJPoNvc7G4wcr2ptKEuzGX0s68yH'

  auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
  client = API(auth) 

  fname = "user_timeline_{}.jsonl".format(user) 
 
  with open(fname, 'w') as f: 
    for page in Cursor(client.user_timeline, screen_name=user,  
                       count=200).pages(16): 
      for status in page: 
      	if (status._json['text'].split(' ')[0] != 'RT'):
          f.write(json.dumps(status._json)+"\n")
