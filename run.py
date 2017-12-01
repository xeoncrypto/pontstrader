#!/usr/bin/python2.7

import sys
import json
import os
from functions import *
import signal
import time

def sigint_handler(signum, frame):
  print 'Stop pressing CTRL+C!'

signal.signal(signal.SIGINT, sigint_handler)

if len(sys.argv) == 2:
  if sys.argv[1] == 'version':
    print 'Version: pontstrader-v3.2'
    sys.exit()
  else:
    print 'Unsupported argument, supported arguments are: version'
    print 'e.g. {0} version'.format(sys.argv[0])
    sys.exit()

try:
  import requests
except ImportError:
  print 'python-requests is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

try:
  from colorama import Fore, Back, Style, init
  init(autoreset=True)
except ImportError:
  print 'python-colorama is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

try:
  import redis
  init(autoreset=True)
except ImportError:
  print 'redis is not installed, please check the docs!'
  print 'https://github.com/p0nt/pontstrader'
  sys.exit()

config_json = (os.path.dirname(os.path.realpath(__file__))) + '/settings.json'
file_exists = os.path.isfile(config_json)

if not file_exists:
  print(Fore.YELLOW + 'It seems that you are running this script for the first time')
  print(Fore.YELLOW + 'or')
  print(Fore.YELLOW + 'If you\'ve upgraded to v3.2, you can copy/paste data from config.json and remove afterwards')
  try:
    print(Fore.YELLOW + 'Step 1: Bittrex API')
    bittrex_key = raw_input('Enter your Bittrex API key : ')
    bittrex_key = str(bittrex_key)
    bittrex_secret = raw_input('Enter your Bittrex API Secret : ')
    bittrex_secret = str(bittrex_secret)
    print(Fore.YELLOW + 'Step 2: Push notifications')
    print (Fore.YELLOW + 'Pushover/Pushbullet allows you to recieve push notifications on your phone for the Trailing Stop feature and future features.')
    print 'Would you like to enable Pushover or Pushbullet?'
    print '1. Pushover'
    print '2. Pushbullet'
    print '3. No'
    print '4. Exit'
    push = raw_input('Enter your choice [1-4] : ')
    push = int(push)
    pushover_user = 'disabled'
    pushover_app = 'disabled'
    pushbullet_token = 'disabled'
    if push == 1:
      pushover_user = raw_input('Enter your Pushover user key : ')
      pushover_user = str(pushover_user)
      pushover_app = raw_input('Enter the Pushover app key : ')
      pushover_app = str(pushover_app)
    elif push == 2:
      pushbullet_token = raw_input('Enter your Pushbullet Access Token : o.')
      pushbullet_token = str(pushbullet_token) 
      pushbullet_token = 'o.{0}'.format(pushbullet_token)
    elif push == 3:
      print 'OK... disabling push notifiations! (remove config.json if you want to re-run the wizard)'
      pushover_user = 'disabled'
      pushover_app = 'disabled'
      pushbullet_token = 'disabled'
    elif push == 4:
      print(Fore.RED + 'Cancelled... unable to finish setup, please try again!')
      sys.exit()
    else:
      print 'Wrong number... disabling push notifications for now! (remove config.json if you want to re-run the wizard)'
      pushover_user = 'disabled'
      pushover_app = 'disabled'
      pushbullet_token = 'disabled'
    print(Fore.YELLOW + 'Step 3: Redis Connection')
    print(Fore.YELLOW + 'Redis a key value database which you have to connect to to make this script work')
    redis_password = raw_input('Enter the Redis password : ')
    redis_password = str(redis_password)
  except:
    print(Fore.RED + 'Cancelled... unable to finish setup, please try again!')
    sys.exit()
  data = { 'bittrex_key' : bittrex_key, 'bittrex_secret' : bittrex_secret, 'pushover_user' : pushover_user, 'pushover_app' : pushover_app, 'pushbullet_token' : pushbullet_token, 'redis_password' : redis_password }
  with open(config_json, 'w') as outfile:
    json.dump(data, outfile)
    outfile.close()
  with open(config_json, 'r') as data_file:
    data = json.load(data_file)
    apikey = str(data['bittrex_key'])
    apisecret = str(data['bittrex_secret'])
    pushover_user = str(data['pushover_user'])
    pushover_app = str(data['pushover_app'])
    pushbullet_token = str(data['pushbullet_token'])
    redis_password = str(data['redis_password'])
  print(Fore.GREEN + 'Setup is done, you can now use pontstrader')
  time.sleep(2)

with open(config_json, 'r') as data_file:
  data = json.load(data_file)
  apikey = str(data['bittrex_key'])
  apisecret = str(data['bittrex_secret'])
  pushover_user = str(data['pushover_user'])
  pushover_app = str(data['pushover_app'])
  pushbullet_token = str(data['pushbullet_token'])
  redis_password = str(data['redis_password'])

menu(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password)
