  #!/usr/bin/env python
  
def balances(key, secret, redis_password):
  
  import time, json, sys, os, redis
  from pprint import pprint
  from time import gmtime, strftime
  from bittrex import bittrex
  from colorama import Fore, Back, Style, init
  init(autoreset=True)

  try:
    r = redis.Redis(host='redis.pontstrader.com', port=6380, db=0, password=redis_password)
  except:
    print 'Unable to connect to redis.pontstrader.com, trying redis2.pontstrader.com...'
    try:
      r = redis.Redis(host='redis2.pontstrader.com', port=6380, db=0, password=redis_password)
    except:
      print 'Unable to connect to redis2.pontstrader.com... I am sorry but you can not continue now, please contact p0nts!'
  
  while True:
    try:
      api = bittrex(key, secret)
    except:
      print 'Bittrex API error: {0}'.format(api)
  
    print (30 * '-')
    print(Fore.GREEN +'   B A L A N C E S')
    print (30 * '-')
    try:
      get_balances = api.getbalances()
      print(Fore.GREEN +'Currency\tBalance\t\t\tAvailable\t\tPending\t\tBTC Value')
      total_btc = 0
      usdt = 0
      for coin in get_balances:
        balance = coin["Balance"]
        if (balance != 0.0 and not None):
          available = coin["Available"]
          currency = coin["Currency"]
          pending = coin["Pending"]
          if currency == 'BTC':
            print ('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}\t{4:.8f}'.format(currency, balance, available, pending, balance))
            last = balance
            total_btc += last
          elif currency == 'USDT':
            print ('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}'.format(currency, balance, available, pending))
            usdt = float(balance)
            last = '0'
          else:
            try:
              market = 'BTC-{0}'.format(currency)
              summary = api.getmarketsummary(market)
              values = r.hmget(market, 'Ask')
              last = float(values[0]) * float(balance)
              total_btc += last
              print ('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}\t{4:.8f}'.format(currency, balance, available, pending, last))
            except:
              print ('{0}\t\t{1:.8f}\t\t{2:.8f}\t\t{3:.8f}'.format(currency, balance, available, pending))
      market = 'USDT-BTC'
      summary = api.getmarketsummary(market)
      total_usd = float(summary[0]['Last']) * float(total_btc) + float(usdt)
      print(Fore.YELLOW +'Estimated Value: {0:.8f} BTC / {1:.8f} USD'.format(total_btc, total_usd))
      output = (Fore.YELLOW +'Refresh: r+enter | Return to Main Menu: q+enter : ')
      refresh = raw_input(output)
      refresh = str(refresh)
      if refresh == 'r':
        print (Fore.GREEN +'Ok, refreshing in 5 seconds... (to prevent spam)')
        time.sleep(5)
      elif refresh == 'q':
        break
      else:
        print 'Invalid input, refreshing in 5 seconds... (to prevent spam)'
        time.sleep(5)
    except:
      print 'Bittrex API error: {0}'.format(get_balances)
      print 'Going back to Main Menu'
      time.sleep(2)
      break
