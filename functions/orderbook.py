#!/usr/bin/env python
  
def orderbook(key, secret, redis_password):
  
  import time, json, sys, redis
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
  
    try:
      openorders = api.getopenorders(market='')
      print (30 * '-')
      print(Fore.GREEN +'   O P E N  O R D E R S')
      print (30 * '-')
      if openorders:
        number = 0
        list = []
        print(Fore.GREEN +'Nr.\tMarket\t\tType\t\tAsk\t\tTotal\t\tFilled\t\tCurrent Ask')
        for order in openorders:
          uuid = order['OrderUuid']
          market = order['Exchange']
          ordertype = order['OrderType']
          total = order['Quantity']
          remaining = order['QuantityRemaining']
          filled = total - remaining
          ask = order['Limit']
          number += 1
          values = r.hmget(market, 'Ask')
          currentprice = float(values[0])
          list.append(uuid)
          if len(market) == 6 or len(market) == 7:
            print '{0}.\t{1}\t\t{2}\t{3:.8f}\t{4:.8f}\t{5:.8f}\t{6:.8f}'.format(number, market, ordertype, ask, total, filled, currentprice)
          else:
            print '{0}.\t{1}\t{2}\t{3:.8f}\t{4:.8f}\t{5:.8f}\t{6:.8f}'.format(number, market, ordertype, ask, total, filled, currentprice)
      else:
        print(Fore.RED +'No open orders found... going back to Main Menu')
        time.sleep(2)
        break
      print(Fore.YELLOW +'To remove an open order, choose the corresponding number.')
      print(Fore.YELLOW +'q+enter to return to Main Menu')
    except:
      print openorders
      print '\nGoing back to Main Menu'
      time.sleep(1)
      break
    try:
      choose_num = raw_input('Enter your choice [1-{0}] : '.format(number))
      choose_num = str(choose_num)
    except:
      print 'Invalid number... going back to Main Menu'
      time.sleep(1)
      break
    try:
      if choose_num == 'q':
        print 'Going back to Main Menu in 2 seconds!'
        time.sleep(2)
        break
      elif choose_num.isdigit():
        choose_num = int(choose_num)
        choose_num = choose_num - 1
        cancel = api.cancel(uuid=list[choose_num])
        print 'Order successfully removed'
        time.sleep(2)
        openorders = api.getopenorders(market='')
      else:
        print 'Going back to Main Menu in 2 seconds!'
        time.sleep(2)
        break
    except:
      print 'Invalid input... going back to Main Menu'
      time.sleep(2)
      break
