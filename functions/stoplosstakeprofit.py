#!/usr/bin/env python
    
def stoplosstakeprofit(key, secret, pushover_user, pushover_app, pushbullet_token, redis_password):

  import sys, os, json, time, threading, requests, redis
  from datetime import datetime
  from bittrex import bittrex
  from pushover import send_pushover
  from pushbullet import send_pushbullet
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

  global messages

  try:
    messages
  except NameError:
    messages = {}
  else:
    pass
  
  print (45 * '-')
  print(Fore.GREEN +'   S T O P  L O S S  T A K E  P R O F I T')
  print (45 * '-')
  while True:
    status_update = False
    gobuy = False
    try:
      threads = threading.enumerate()
      thread_counter = 0
      for t in threading.enumerate():
        if t.name.startswith('sltp-'):
          thread_counter += 1
      if thread_counter > 0:
        print (Fore.YELLOW +'There are currently {0} active sltp trade(s):'.format(thread_counter))
      else:
        print (Fore.YELLOW +'There are currently no active sltp trades')
      print 'Would you like to make another sltp trade or check the status/history of your sltp trades?'
      print(Fore.GREEN +'1. New trade')
      print(Fore.YELLOW +'2. Status / History')
      print(Fore.RED +'3. Back to Main Menu')
      try:
        yes_no = raw_input('Enter your choice [1-3] : ')
        yes_no = int(yes_no)
        print (40 * '-')
      except:
        print '\nInvalid number... going back to Main Menu'
        time.sleep(1)
        break
      if yes_no == 1:
        pass
      elif yes_no == 2:
        while True:
          try:
            trades = 0
            for k, v in messages.iteritems():
              trades += 1
              if v.startswith('sltp-'):
                print v
            if trades == 0:
              print (Fore.RED +'There is currently no sltp trade status/history available!')
              print (40 * '-')
            print 'Refresh, new trade or back to Main Menu?' 
            print(Fore.GREEN +'1. Refresh')
            print(Fore.YELLOW +'2. New Trade')
            print(Fore.RED +'3. Back to Main Menu')
            go_break = False
            try:
              yes_no = raw_input('Enter your choice [1-3] : ')
              yes_no = int(yes_no)  
              print (40 * '-')
            except:
              go_break = True
              print '\nInvalid number... going back to Main Menu'
              time.sleep(1)
              break
            if yes_no == 1:
              pass
            elif yes_no == 2:
              break
            elif yes_no == 3:
              print '\nOk... going back to Main Menu'
              time.sleep(1)
              break
            else:
              go_break = True
              print '\nInvalid number... going back to Main Menu'
              time.sleep(1)
              break
          except:
            print (Fore.RED +'\nUnable to retrieve active threads data... going back to Main Menu')
            break
        if yes_no == 3 or go_break == True:
          break
      elif yes_no == 3:
        print '\nOk... going back to Main Menu'
        time.sleep(1)
        break
      else:
        print '\nInvalid number... going back to Main Menu'
        time.sleep(1)
        break
    except:
      print (Fore.RED +'\nUnable to retrieve active threads... there is something wrong please contact p0nts!')
      break
   
    try:
      market = raw_input('Market? (e.g. BTC-NEO / ETH-LTC / USDT-OMG) : ')
      market = str(market.upper())
      trade = market.split('-')[0]
      currency = market.split('-')[1]
      check_status = r.exists(market)
      if check_status != True:
        print 'Unsupported market... going back to Main Menu'
        time.sleep(1)
        break
    except:
      print '\nInvalid input... going back to Main Menu'
      time.sleep(1)
      break

    if market.startswith('BTC'):
      trade = 'BTC'
    elif market.startswith('ETH'):
      trade = 'ETH'
    elif market.startswith('USDT'):
      trade = 'USDT'
    else:
      print 'Unsupported market... going back to Main Menu'
      time.sleep(1)
      break
  
    try:
      value = raw_input('How much {0}? (excl. fee) : '.format(trade))
      value = float(value)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    else:
      try:
        api = bittrex(key, secret)
        available = api.getbalance(trade)
      except:
        print (Fore.RED +'Unable to retrieve balance information from Bittrex... going back to Main Menu')
        time.sleep(1)
        break
      else:
        if float(value) > float(available['Available']):
          print (Fore.RED +'You have less {0} balance available than you want to trade with... going back to Main Menu'.format(trade))
          time.sleep(1)
          break

    oneortwotargets = False
    if value < 0.00100000:
      print (Fore.RED +'The minimum trade size on Bittrex is 100k sat')
      time.sleep(1)
      break
#    elif value >= 0.00200000:
#      print (Fore.GREEN +'You are trading more than or equal to 200k satoshi, which means you are eligible to use multiple sell targets due to Bittrex new policy of 100k satoshi minimum per trade.')
#      print (Fore.GREEN +' - One sell target = sell 100% at .. satoshi')
#      print (Fore.GREEN +' - Two sell targets = sell 50% at .. satoshi, and the other 50% at x satoshi')
#      print (40 * '-')
#      print (Fore.YELLOW +'Would you like to use 2 sell targets or just one?')
#      print (Fore.GREEN +'1. yes, two')
#      print (Fore.YELLOW +'2. no, just one')
#      print (Fore.RED +'3. Return to Main Menu')
#      try:
#        oneortwo = raw_input('Enter your choice [1-3] : ')
#        oneortwo = int(oneortwo)
#      except:
#        print '\nCancelled... going back to Main Menu'
#        time.sleep(1)
#        break
#      if oneortwo == 1:
#        oneortwotargets = True
#      elif oneortwo == 2:
#        pass
#      elif oneortwo == 3:
#        print 'Ok... going back to Main Menu'
#        time.sleep(1)
#        break
#      else:
#        print '\nInvalid number... going back to Main Menu'
#        time.sleep(1)
#        break
    else:
      print (Fore.YELLOW +'You are trading with less than 200k satoshi, which means you are not eligible to use multiple sell targets due to Bittrex new policy of 100k satoshi per trade minimum, so we will stick with one.')

    try:
      values = r.hmget(market, 'Ask', 'MarketName', 'BaseVolume', 'Volume', 'OpenBuyOrders', 'OpenSellOrders', 'High', 'Low', 'Last', 'Bid')
    except:
      print 'API error: Unable to retrieve pricing information for redis.pontstrader.com... going back to Main Menu'
      time.sleep(1)
      break

    print (40 * '-')
    print (Fore.GREEN +'   M A R K E T  I N F O R M A T I O N')
    print (40 * '-')
    print (Fore.YELLOW +'- Market:           {0}'.format(market))
    print (Fore.YELLOW +'- Volume:           {0:.8f}'.format(float(values[2])))
    print (Fore.YELLOW +'- 24H volume:       {0:.8f}'.format(float(values[3])))
    print (Fore.YELLOW +'- Open buy orders:  {0}'.format(values[4]))
    print (Fore.YELLOW +'- Open sell orders: {0}'.format(values[5]))
    print (Fore.YELLOW +'- 24H high:         {0:.8f}'.format(float(values[6])))
    print (Fore.YELLOW +'- 24H low:          {0:.8f}'.format(float(values[7])))
    print (Fore.YELLOW +'- Last:             {0:.8f}'.format(float(values[8])))
    print (Fore.YELLOW +'- Ask:              {0:.8f}'.format(float(values[0])))
    print (Fore.YELLOW +'- Bid:              {0:.8f}'.format(float(values[9])))
    print (40 * '-')
    try:
      stoploss = raw_input('Stop Loss? [eg. 0.00436] : ')
      stoploss = float(stoploss)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break

    if oneortwotargets == True:
      pass
#      try:
#        target1 = raw_input('Target 1? 50% of the trade value will be sold here [eg. 0.00436] : ')
#        target1 = float(target1)
#      except:
#        print '\nInvalid number... going back to Main Menu'
#        time.sleep(1)
#        break
#
#      try:
#        target2 = raw_input('Target 2? 50% of the trade value will be sold here [eg. 0.00436] : ')
#        target2 = float(target2)
#      except:
#        print '\nInvalid number... going back to Main Menu'
#        time.sleep(1)
#        break
#      print (40 * '-')
#      print (Fore.GREEN +'   B U Y  I N F O R M A T I O N')
#      print (Fore.YELLOW +'- Buyprice:               {0:.8f}'.format(float(values[0])))
#      print (Fore.YELLOW +'- Target 1:               {0:.8f}'.format(float(target1)))
#      print (Fore.YELLOW +'- Target 2:               {0:.8f}'.format(float(target2)))
#      print (Fore.YELLOW +'- Stop Loss:              {0:.8f}'.format(float(stoploss)))
#      print (Fore.YELLOW +'Because the price could have changed during your input...')
#      print (Fore.YELLOW +'Pontstrader wil calculate new targets and stop loss based on the buyprice.')
    else:
      try:
        target = raw_input('Target? 100% of the trade value will be sold here [eg. 0.00436] : ')
        target = float(target)
      except:
        print '\nInvalid number... going back to Main Menu'
        time.sleep(1)
        break
      print (40 * '-')
      print (Fore.GREEN +'   B U Y  I N F O R M A T I O N')
      print (Fore.YELLOW +'- Buyprice:               {0:.8f}'.format(float(values[0])))
      print (Fore.YELLOW +'- Target:                 {0:.8f}'.format(float(target)))
      print (Fore.YELLOW +'- Stop Loss:              {0:.8f}'.format(float(stoploss)))
      print (40 * '-')
      print (Fore.YELLOW +'Because the price could have changed during your input, the buyprice may differ a little from the above prices!')
    
    print (40 * '-')
    print 'Proceed?'
    print (Fore.GREEN +'1. yes')
    print (Fore.RED +'2. no, return to Main Menu')
    try:
      proceed = raw_input('Enter your choice [1-2] : ')
      proceed = int(proceed)
    except:
      print '\nCancelled... going back to Main Menu'
      time.sleep(1)
      break
    if proceed == 1:
      try:
        values = r.hmget(market, 'Ask')
        ask = float(values[0])
        amount = float(value) / float(ask)
        orderbook = api.getorderbook(market, type='sell')
        orderbook_rate = orderbook[0]['Rate']
        orderbook_quantity = orderbook[0]['Quantity']
        if float(amount) < float(orderbook_quantity):
          gobuy = True
          break
        else:
          while float(amount) > float(orderbook_quantity):
            time.sleep(1)
            orderbook = api.getorderbook(market, type='sell')
            orderbook_rate = orderbook[0]['Rate']
            orderbook_quantity = orderbook[0]['Quantity']
            values = r.hmget(market, 'Ask')
            ask = float(values[0])
            amount = float(value) / float(ask)
            print (Fore.YELLOW +'Waiting for the volume to rise on lowest Ask to buy all for the same price.')
          gobuy = True
          break
      except:
        print 'API error: Unable to create a buyorder... going back to Main Menu'
        time.sleep(1)
        break
    elif proceed == 2:
      print 'Ok... going back to Main Menu'
      time.sleep(1)
      break
    else:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break

  if gobuy == True:
    def start_thread_single(market, currency, amount, ask, stoploss, target):
      time.sleep(1)
      global messages
      thread_name = threading.current_thread().name
      done = False
      while True:
        values = r.hmget(market, 'Ask')
        ask = float(values[0])
        try:
          buy = api.buylimit(market, amount, ask)
        except:
          message = 'Bittrex API error, unable to buy: {0}'.format(buy)
          messages[thread_name] = message
          send_pushover(pushover_user, pushover_app, message)
          send_pushbullet(pushbullet_token, message)
          break
        else:
          time.sleep(0.5)
          buy_uuid = buy['uuid']
          time.sleep(0.5)
          push_send = False
          try:
            buyorder = api.getorder(uuid=buy_uuid)
          except:
            message = 'Bittrex API error, unable to check the buyorder: {0}'.format(buyorder)
            messages[thread_name] = message
          else:
            if buyorder['IsOpen'] == True:
              while buyorder['IsOpen'] == True:
                message = '{0}: Made a buyorder, waiting until it is filled! Remaining: {1:.8f} {2}'.format(thread_name, buyorder['QuantityRemaining'], currency)
                messages[thread_name] = message
                if push_send == False:
                  try:
                    send_pushover(pushover_user, pushover_app, message)
                    send_pushbullet(pushbullet_token, message)
                    push_send = True
                  except:
                    message = 'Unable to send push notification with the buyorder status'
                    messages[thread_name] = message
                try:
                  buyorder = api.getorder(uuid=buy_uuid)
                except:
                  message = 'Bittrex API error, unable to check the buyorder: {0}'.format(buyorder)
                  messages[thread_name] = message
                  pass
                time.sleep(10)
            buyprice = float(ask)
            lastprice = 0
          while True:
            try:
              time.sleep(0.5)
              values = r.hmget(market, 'Ask')
              ask = float(values[0])
            except:
              message = 'Unable to retrieve data from redis.pontstrader.com, trying to recover...'
              messages[thread_name] = message
            else:
              profit_percentage = 100 * (float(ask) - float(buyprice)) / float(buyprice)
              if float(ask) >= float(target):
                try:
                  sell = api.selllimit(market, amount, target)
                  sell_uuid = sell['uuid']
                  time.sleep(0.5)
                  sellorder = api.getorder(uuid=sell_uuid)
                  if sellorder['IsOpen'] == True:
                    while sellorder['IsOpen'] == True:
                      message = '{0}: Sell target triggered, waiting until the sell order is completely filled! Remaining: {1:.8f}'.format(thread_name, sellorder['QuantityRemaining'])
                      messages[thread_name] = message
                      try:
                        sellorder = api.getorder(uuid=sell_uuid)
                      except:
                        pass
                      time.sleep(2)
                  message = '{0}: {1} SOLD (Target) | Buy price {2:.8f} | Sell price {3:.8f} | Profit {4:.2f}% (excl. fee)'.format(thread_name, currency, buyprice, target, profit_percentage)
                  messages[thread_name] = message
                  send_pushover(pushover_user, pushover_app, message)
                  send_pushbullet(pushbullet_token, message)
                  done = True
                  break
                except:
                  message = '{0}: API error: Was unable to create the sellorder... it was cancelled due to:\n{1}'.format(thread_name, sell)
                  messages[thread_name] = message
                  send_pushover(pushover_user, pushover_app, message)
                  send_pushbullet(pushbullet_token, message)
                  done = True
                  break
              elif float(ask) <= float(stoploss):
                try:
                  sell = api.selllimit(market, amount, stoploss)
                  sell_uuid = sell['uuid']
                  time.sleep(0.5)
                  sellorder = api.getorder(uuid=sell_uuid)
                  if sellorder['IsOpen'] == True:
                    while sellorder['IsOpen'] == True:
                      message = '{0}: Stop Loss triggered, waiting until the sell order is completely filled! Remaining: {1:.8f}'.format(thread_name, sellorder['QuantityRemaining'])
                      messages[thread_name] = message
                      try:
                        sellorder = api.getorder(uuid=sell_uuid)
                      except:
                        pass
                      time.sleep(2)
                  message = '{0}: {1} SOLD (Stop Loss) | Buy price {2:.8f} | Sell price {3:.8f} | Loss {4:.2f}% (excl. fee)'.format(thread_name, currency, buyprice, stoploss, profit_percentage)
                  messages[thread_name] = message
                  send_pushover(pushover_user, pushover_app, message)
                  send_pushbullet(pushbullet_token, message)
                  done = True
                  break
                except:
                  message = '{0}: API error: Was unable to create the sellorder... it was cancelled due to:\n{1}'.format(thread_name, sell)
                  messages[thread_name] = message
                  send_pushover(pushover_user, pushover_app, message)
                  send_pushbullet(pushbullet_token, message)
                  done = True
                  break
              else:
                message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Target: {4:.8f} | Profit {5:.2f}% (excl. fee)'.format(thread_name, currency, buyprice, ask, target, profit_percentage)
                messages[thread_name] = message

        if done == True:
          break
    try:
      datetime = datetime.now().strftime("%d-%m-%Y.%H:%M")
      threadname = 'sltp-{0}'.format(datetime)
      if oneortwotargets == True:
        thread = threading.Thread(name=threadname, target=start_thread,args=(market, currency, amount, ask, stoploss, target1, target2))
      else:
        thread = threading.Thread(name=threadname, target=start_thread_single,args=(market, currency, amount, ask, stoploss, target))
      thread.daemon = True
      thread.start()
      print (Fore.GREEN +'Made a buy order, to check its status go to the Stop Loss Take Profit menu again... going back to Main Menu in 2 seconds')
      time.sleep(2)
    except:
      print (Fore.RED +'Unable to start thread... there is something wrong please contact p0nts!')
