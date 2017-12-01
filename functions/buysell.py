  #!/usr/bin/env python
  
def buysell(key, secret, redis_password):
  
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
      time.sleep(2)
      break
  
    print (30 * '-')
    print(Fore.GREEN +'   B U Y  A N D  S E L L')
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
      time.sleep(2)
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
      print 'Unable to retrieve latest pricing from redis.pontstrader.com'
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
        print 'ERROR: Please select a number!'
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
    try:
      multiplier = float(raw_input('Multiplier? [1.1 / 1.3] (1.1 = 10%) : '))
      multiprice = round(buy_for*multiplier, 8)
      multitotal = float(amount) * float(multiprice)
      total = float(amount) * float(buy_for)
      print (30 * '-')
      print(Fore.GREEN +'Going to add a buy order for {0:.8f} {1} at {2:.8f} {3} each (total: {4:.8f} {3})'.format(amount, currency, buy_for, trade, total))
      print(Fore.GREEN +'Going to add a sell order for {0:.8f} {1} at {2:.8f} {3} each (total: {4:.8f} {3})'.format(amount, currency, multiprice, trade, multitotal))
    except:
      print 'ERROR: Amount must be a number!'
  
    print (30 * '-')
    print 'Proceed?'
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
        print apicall['uuid']
        uuid = apicall['uuid']
        total = amount * buy_for
        print(Fore.GREEN +'Added a buy order for {0:.8f} {1} at {2:.8f} {3} each which is {4:.8f} {3} total'.format(amount, currency, buy_for, trade, total))
      except:
        print 'Bittrex API error: {0}'.format(apicall)
        print 'Going back to Main Menu'
        time.sleep(2)
        break
      print(Fore.YELLOW +'Waiting up to 60 seconds for the buy order to be filled...')
      print(Fore.YELLOW +'If the buy order will not be filled for 100% I am unable to add the sell order...')
      t_end = time.time() + 60
      orderstatus = api.getorder(uuid=uuid)
      while orderstatus['QuantityRemaining'] != 0.0 and time.time() < t_end:
        orderstatus = api.getorder(uuid=uuid)
        if orderstatus['QuantityRemaining'] == 0.0:
          print 'Great, order is completely filled!'
          try:
            apicall = api.selllimit(market, amount, multiprice)
          except:
            print 'Bittrex API error: {0}'.format(apicall)
            print 'Going back to Main Menu'
            time.sleep(2)
            break
          print apicall['uuid']
          total = amount * multiprice
          print(Fore.GREEN +'Added a sell order for {0:.8f} {1} at {2:.8f} {3} each which is {4:.8f} {3} total'.format(amount, currency, multiprice, trade, total))
          print 'Returning to Main Menu in 2 seconds...'
          time.sleep(2)
          break
        else:
          time.sleep(10)
      print(Fore.RED +'Unable to add a sell order, because the buy order is not \'completely\' filled, You will have to do this manually as soon as the buy order is completely filled!')
      print(Fore.YELLOW +'Please keep in mind the buy order remains untill cancelled or filled!')
      print 'Returning to Main Menu in 2 seconds...'
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
