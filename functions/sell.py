#!/usr/bin/env python
  
def sell(key, secret, redis_password):
  
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
      currencies = api.getcurrencies()
      markets = api.getmarkets()
    except:
      print 'Bittrex API error: {0}'.format(api)
      print 'Going back to Main Menu'
      time.sleep(1)
      break
  
    print (30 * '-')
    print(Fore.GREEN +'   S E L L  O R D E R')
    print (30 * '-')
    try:
      balances = api.getbalances()
      print(Fore.GREEN +'Currency\tAvailable')
      number = 0
      list = []
      for coin in balances:
        available = coin["Available"]
        currency = coin["Currency"]
        if available != 0.0 and not None:
          number += 1
          list.append(currency)
          if len(currency) < 5:
            print '{0}. {1}\t\t{2:.8f}'.format(number, currency, available)
          else:
            print '{0}. {1}\t{2:.8f}'.format(number, currency, available)
    except:
      print 'Bittrex API error: {0}'.format(balances)
      print 'Going back to Main Menu'
      time.sleep(2)
      break
    try:
      choose_num = raw_input('Enter your choice [1-{0}] (q+enter to return to Main Menu) : '.format(number))
      choose_num = int(choose_num)
    except:
      print 'Going back to Main Menu'
      time.sleep(1)
      break
    try:
      choose_num = choose_num - 1
      if choose_num == -1:
        print 'Invalid number... going back to Main Menu'
        time.sleep(1)
        break
      print(Fore.GREEN +'Starting sell for {0}'.format(list[choose_num]))
      print (30 * '-')
      print ('Market?')
      print(Fore.YELLOW +'1. BTC')
      print(Fore.YELLOW +'2. ETH')
      print(Fore.YELLOW +'3. USDT')
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    try:
      trade = raw_input('Enter your choice [1-3] : ')
      trade = int(trade)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    if trade == 1:
      trade = 'BTC'
    elif trade == 2:
      trade = 'ETH'
    elif trade == 3:
      trade = 'USDT'
    else:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    try:
      currency = list[choose_num]
      market = '{0}-{1}'.format(trade, currency)
    except:
      print available
      print '\nGoing back to Main Menu'
      time.sleep(1)
      break
    try:
      values = r.hmget(market, 'Last', 'Bid', 'Ask')
      balance = api.getbalance(currency)
      last = float(values[0])
      bid = float(values[1])
      ask = float(values[2])
      print (30 * '-')
      print '- Available:\t {0:.8f} {1}'.format(balance['Available'], currency)
      print '- Price (Last):  {0:.8f} {1}'.format(last, trade)
      print '- Price (Bid):\t {0:.8f} {1}'.format(bid, trade)
      print '- Price (Ask):\t {0:.8f} {1}'.format(ask, trade)
    except:
      print 'Unable to retrieve data from redis.pontstrader.com'
      print 'Going back to Main Menu'
      time.sleep(2)
      break
    for f in currencies:
      if f['Currency'] == currency:
        fee = f['TxFee']
        print '- Fee:\t\t {0:.8f} {1}'.format(fee, currency)
    for m in markets:
      if m['MarketCurrency'] == currency and m['BaseCurrency'] == trade:
        minimum = m['MinTradeSize']
        print '- Minimum ({0}): {1:.8f}'.format(currency, minimum)
    #print '- Minimum ({0}): 0.00100000'.format(trade)
    enough = balance['Available'] - fee
    if enough < 0.00000001:
      print(Fore.RED +'You dont have enough {0} ({1:.8f}) to sell anything!'.format(currency, enough))
      time.sleep(1)
      break
    else:
      print(Fore.GREEN +'You have {0:.8f} {1}'.format(balance['Available'], currency))
      print (30 * '-')
      print ('Sellprice?')
      print(Fore.YELLOW +'1. Last ({0:.8f} {1})'.format(last, trade))
      print(Fore.YELLOW +'2. Bid ({0:.8f} {1})'.format(bid, trade))
      print(Fore.YELLOW +'3. Ask ({0:.8f} {1})'.format(ask, trade))
      print(Fore.YELLOW +'4. Custom')
      print(Fore.RED +'5. Back to Main Menu') 
      try:
        sellprice = raw_input('Enter your choice [1-5] : ')
        sellprice = int(sellprice)
      except:
        print '\nInvalid number... going back to Main Menu'
        time.sleep(1)
        break
      if sellprice == 1:
        sell_for = last
        print 'Selected \'Last\': {0:.8f} {1}'.format(last, trade)
      elif sellprice == 2:
        sell_for = bid
        print 'Selected \'Bid\': {0:.8f} {1}'.format(bid, trade)
      elif sellprice == 3:
        sell_for = ask
        print 'Selected \'Ask\': {0:.8f} {1}'.format(ask, trade)
      elif sellprice == 4:
        try:
          sell_for = raw_input('Sellprice? e.g. [0.00000001] : ')
          sell_for = float(sell_for)
          print 'Selected \'Custom\': {0:.8f} {1}'.format(sell_for, trade)
        except:
          print 'Please provide a proper sellprice! (e.g. {0:.8f})'.format(last)
          print 'Going back to Main Menu'
          time.sleep(1)
          break
      elif sellprice == 5:
        break
      else:
        print '\nInvalid number... going back to Main Menu'
        time.sleep(1)
        break
    try:
      amount = raw_input('Amount? : ')
      amount = float(amount)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    print (30 * '-')
    print ('Selling {0:.8f} {1} for {2:.8f} {3} each, Proceed?'.format(amount, currency, sell_for, trade))
    print(Fore.GREEN +'1. yes')
    print(Fore.RED +'2. no (Back to Main Menu)')
    try:
      yes_no = raw_input('Enter your choice [1-2] : ')
      yes_no = int(yes_no)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    if yes_no == 1:
      try:
        apicall = api.selllimit(market, amount, sell_for)
        sell_uuid = apicall['uuid']
        time.sleep(0.5)
        sellorder = api.getorder(uuid=sell_uuid)
        total = amount * sell_for
        print(Fore.GREEN +'Added a sell order for {0:.8f} {1} at {2:.8f} {3} each which is {4:.8f} {3} total'.format(amount, currency, sell_for, trade, total))
        print 'Checking status in 2 seconds'
        time.sleep(2)
        if sellorder['IsOpen'] == False:
          print 'Great! Order is completely filled'
        else:
          print ('Order is not filled yet, would you like to wait up to 120 seconds?'.format(amount, sell_for, trade))
          print (Fore.GREEN +'1. yes')
          print(Fore.RED +'2. no (Back to Main Menu)')
          try:
            yes_no = raw_input('Enter your choice [1-2] : ')
            yes_no = int(yes_no)
          except:
            print '\nInvalid number... going back to Main Menu'
            time.sleep(1)
            break
          if yes_no == 1:
            print (Fore.YELLOW +'Script will automatically return to Main Menu after 120 seconds')
            time_decrease = 120
            if sellorder['IsOpen'] == True:
              while sellorder['IsOpen'] == True:
                if time_decrease <= 0:
                  break
                print (Fore.YELLOW +'Waiting until the sell order is completely filled! Remaining: {0:.8f} ({1} seconds remaining)'.format(sellorder['QuantityRemaining'], time_decrease))
                sellorder = api.getorder(uuid=sell_uuid)
                time.sleep(10)
                time_decrease -= 10
              print 'Unfortunatly the order is not completely filled yet'
            else:
              print 'Great! Order is completely filled'
          elif yes_no == 2:
            print '\nOk... going back to Main Menu'
            time.sleep(1)
            break
          else:
            print '\nInvalid number... going back to Main Menu'
            time.sleep(1)
            break
        print 'Returning to Main Menu in 2 seconds...'
        time.sleep(2)
        break
      except:
        print 'Bittrex API error: {0}'.format(apicall)
        print 'Going back to Main Menu'
        time.sleep(2)
        break
    elif yes_no == 2:
      print '\nGoing back to Main Menu'
      time.sleep(1)
      break
    else:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
