#!/usr/bin/env python

def send_pushover(pushover_user, pushover_app, message):

  import requests

  if pushover_user == 'disabled' or pushover_app == 'disabled':
    pass
  else:
    payload = {"message": message, "user": pushover_user, "token": pushover_app }
    r = requests.post('https://api.pushover.net/1/messages.json', data=payload, headers={'User-Agent': 'Python'})
    if r.status_code != 200:
      print 'ERROR: Unable to send pushover (status code: {0} | error: {1})'.format(r.status_code, r)
