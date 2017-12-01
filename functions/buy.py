#!/usr/bin/env python

def buy(key, secret, redis_password):

  import time, json, sys, redis
  from pprint import pprint
  from time import gmtime, strftime
  from bittrex import bittrex
  from menu import menu
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
      time.sleep(2)
      break

    print (30 * '-')
    print(Fore.GREEN +'   B U Y  O R D E R')
    print (30 * '-')
    print ('Market?')
    print(Fore.YELLOW +'1. BTC')
    print(Fore.YELLOW +'2. ETH')
    print(Fore.YELLOW +'3. USDT')
    print(Fore.RED +'4. Back to Main Menu')
    try:
      trade = raw_input('Enter your choice [1-4] : ')
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
    elif trade == 4:
      break
    else:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    try:
      currency = raw_input('Currency? (e.g. LTC / NEO / OMG) : ').upper()
    except:
      print 'Invalid currency... going back to Main Menu'
      time.sleep(1)
      break
    try:
      market = '{0}-{1}'.format(trade, currency)
      available = api.getbalance(trade)
    except:
      print available
      print '\nGoing back to Main Menu'
      time.sleep(1)
      break
    try:
      values = r.hmget(market, 'Last', 'Bid', 'Ask')
      last = float(values[0])
      bid = float(values[1])
      ask = float(values[2])
      print (30 * '-')
      print '- Price (Last): {0:.8f} {1}'.format(last, trade)
      print '- Price (Bid): {0:.8f} {1}'.format(bid, trade)
      print '- Price (Ask): {0:.8f} {1}'.format(ask, trade)
    except:
      print 'Unable to retrieve data from redis.pontstrader.com (Unsupported Market?)'
      print 'Going back to Main Menu'
      time.sleep(2)
      break
    for f in currencies:
      if f['Currency'] == currency:
        fee = f['TxFee']
        trade_fee = last * fee
        print '- Fee {0:.8f} {1} ({2:.8f} {3})'.format(fee, currency, trade_fee, trade)
    for m in markets:
      if m['MarketCurrency'] == currency and m['BaseCurrency'] == trade:
        minimum = m['MinTradeSize']
        print '- Minimum ({0}): {1:.8f}'.format(currency, minimum)
    print '- Minimum ({0}): 0.00100000'.format(trade)
    enough = trade_fee + 0.00100000 + last
    if available['Available'] < 0.00100000:
      print(Fore.RED +'You dont have enough {0} ({1:.8f}) to buy anything!'.format(trade, available['Available']))
      time.sleep(1)
      break
    else:
      available_after_fee = available['Available'] - trade_fee
      print(Fore.YELLOW +'You have {0:.8f} {1} available in total'.format(available['Available'], trade))
      print(Fore.YELLOW +'Which is {0:.8f} {1} exclusive required fee'.format(available_after_fee, trade))
      can_buy_last = available_after_fee / last
      can_buy_bid = available_after_fee / bid
      can_buy_ask = available_after_fee / ask
      print(Fore.GREEN +'You can buy up to {0:.8f} {1} for \'Last\' price'.format(can_buy_last, currency))
      print(Fore.GREEN +'You can buy up to {0:.8f} {1} for \'Bid\' price'.format(can_buy_bid, currency))
      print(Fore.GREEN +'You can buy up to {0:.8f} {1} for \'Ask\' price'.format(can_buy_ask, currency))
      print (30 * '-')
      print ('Buyprice?')
      print(Fore.YELLOW +'1. Last ({0:.8f} {1})'.format(last, trade))
      print(Fore.YELLOW +'2. Bid ({0:.8f} {1})'.format(bid, trade))
      print(Fore.YELLOW +'3. Ask ({0:.8f} {1})'.format(ask, trade))
      print(Fore.YELLOW +'4. Custom')
      print(Fore.RED +'5. Back to Main Menu')
      try:
        buyprice = raw_input('Enter your choice [1-5] : ')
        buyprice = int(buyprice)
      except:
        print '\nInvalid number... going back to Main Menu'
        time.sleep(1)
        break
      if buyprice == 1:
        buy_for = last
        print 'Selected \'Last\': {0:.8f} {1}'.format(last, trade)
      elif buyprice == 2:
        buy_for = bid
        print 'Selected \'Bid\': {0:.8f} {1}'.format(bid, trade)
      elif buyprice == 3:
        buy_for = ask
        print 'Selected \'Ask\': {0:.8f} {1}'.format(ask, trade)
      elif buyprice == 4:
        try:
          buy_for = raw_input('Buyprice? e.g. [0.00000001] : ')
          buy_for = float(buy_for)
          print 'Selected \'Custom\': {0:.8f} {1}'.format(buy_for, trade)
        except:
          print 'Please provide a proper buyprice! (e.g. {0:.8f})'.format(last)
          print 'Invalid number... going back to Main Menu'
          time.sleep(2)
          break
      elif buyprice == 5:
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
    print ('Buying {0:.8f} for {1:.8f} {2} each, Proceed?'.format(amount, buy_for, trade))
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
        apicall = api.buylimit(market, amount, buy_for)
        buy_uuid = apicall['uuid']
        time.sleep(0.5)
        buyorder = api.getorder(uuid=buy_uuid)
        total = amount * buy_for
        print(Fore.GREEN +'Added a buy order for {0:.8f} {1} at {2:.8f} {3} each which is {4:.8f} {3} total'.format(amount, currency, buy_for, trade, total))
        print 'Checking status in 2 seconds'
        time.sleep(2)
        if buyorder['IsOpen'] == False:
          print 'Great! Order is completely filled'
        else:
          print ('Order is not filled yet, would you like to wait up to 120 seconds?'.format(amount, buy_for, trade)) 
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
            time_count = 0
            time_decrease = 120
            if buyorder['IsOpen'] == True:
              while buyorder['IsOpen'] == True:
                if time_count >= 120:
                  break
                print (Fore.YELLOW +'Waiting until the buy order is completely filled! Remaining: {0:.8f} ({1} seconds remaining)'.format(buyorder['QuantityRemaining'], time_decrease))
                buyorder = api.getorder(uuid=buy_uuid)
                time.sleep(10)
                time_decrease -= 10
                time_count += 10
              print 'Unfortunatly the order is not completely filled yet'
            else:
              print 'Great! Order is completely filled'
              time.sleep(1)
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
      print '\nCancelled... going back to Main Menu'
      time.sleep(1)
      break
    else:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
