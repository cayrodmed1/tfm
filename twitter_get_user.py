import os 
import sys 
import json 
import time 
import math 
from tweepy import Cursor, API, OAuthHandler
 
MAX_FRIENDS = 15000 
 
def usage(): 
  print("Usage:") 
  print("python {} <username>".format(sys.argv[0])) 
 
def paginate(items, n): 
  """Generate n-sized chunks from items""" 
  for i in range(0, len(items), n): 
    yield items[i:i+n] 
 
if __name__ == '__main__': 
  if len(sys.argv) != 2: 
    usage() 
    sys.exit(1) 
  screen_name = sys.argv[1]

  ACCESS_TOKEN = '381520903-OwPTkjllzq7T9cmeuloBQzUVUBxjjjD3c3YjBB18'
  ACCESS_SECRET = 'lOBE3wrQZWuPvDoiF4vhfhCZB3oiRbFTArdVmf2CZDBqC'
  CONSUMER_KEY = 'KLRKa701PFkAboW9wMhACOa1x'
  CONSUMER_SECRET = 'OlREM6mGWSy7JvBEhjl4mhtJPoNvc7G4wcr2ptKEuzGX0s68yH'

  auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
  client = API(auth) 
  dirname = "users/{}".format(screen_name) 
  max_pages = math.ceil(MAX_FRIENDS / 5000) 
  try: 
    os.makedirs(dirname, mode=0o755, exist_ok=True) 
  except OSError: 
    print("Directory {} already exists".format(dirname)) 
  except Exception as e: 
    print("Error while creating directory {}".format(dirname)) 
    print(e) 
    sys.exit(1) 
 
  # get followers for a given user 
  fname = "users/{}/followers.jsonl".format(screen_name) 
  with open(fname, 'w') as f: 
    for followers in Cursor(client.followers_ids,  
                            screen_name=screen_name).pages(max_pages): 
      for chunk in paginate(followers, 100): 
        users = client.lookup_users(user_ids=chunk) 
        for user in users: 
          f.write(json.dumps(user._json)+"\n") 
      if len(followers) == 5000: 
        print("More results available. Sleeping for 60 seconds to  avoid rate limit") 
        time.sleep(60) 
 
  # get friends for a given user 
  fname = "users/{}/friends.jsonl".format(screen_name) 
  with open(fname, 'w') as f: 
    for friends in Cursor(client.friends_ids,  
                          screen_name=screen_name).pages(max_pages): 
      for chunk in paginate(friends, 100): 
        users = client.lookup_users(user_ids=chunk) 
        for user in users: 
          f.write(json.dumps(user._json)+"\n") 
      if len(friends) == 5000: 
        print("More results available. Sleeping for 60 seconds to avoid rate limit")
        time.sleep(60) 
 
  # get user's profile 
  fname = "users/{}/user_profile.json".format(screen_name) 
  with open(fname, 'w') as f: 
    profile = client.get_user(screen_name=screen_name) 
    f.write(json.dumps(profile._json, indent=4))