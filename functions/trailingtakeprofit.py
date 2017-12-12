#!/usr/bin/env python
    
def trailingtakeprofit(key, secret, pushover_user, pushover_app, pushbullet_token, redis_password):

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
  
  print (40 * '-')
  print(Fore.GREEN +'   T R A I L I N G  T A K E  P R O F I T')
  print (40 * '-')
  while True:
    status_update = False
    gobuy = False
    try:
      threads = threading.enumerate()
      thread_counter = 0
      for t in threading.enumerate():
        if t.name.startswith('ttp-'):
          thread_counter += 1
      if thread_counter > 0:
        print (Fore.YELLOW +'There are currently {0} active ttp trade(s):'.format(thread_counter))
      else:
        print (Fore.YELLOW +'There are currently no active ttp trades')
      print 'Would you like to make another ttp trade or check the status/history of your ttp trades?'
      print(Fore.GREEN +'1. New trade')
      print(Fore.YELLOW +'2. Status / History')
      print(Fore.RED +'3. Back to Main Menu')
      try:
        yes_no = raw_input('Enter your choice [1-3] : ')
        yes_no = int(yes_no)
        print (30 * '-')
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
              if v.startswith('ttp-'):
                print v
            if trades == 0:
              print (Fore.RED +'There is currently no ttp trade status/history available!')
              print (30 * '-')
            print 'Refresh, new trade or back to Main Menu?' 
            print(Fore.GREEN +'1. Refresh')
            print(Fore.YELLOW +'2. New Trade')
            print(Fore.RED +'3. Back to Main Menu')
            go_break = False
            try:
              yes_no = raw_input('Enter your choice [1-3] : ')
              yes_no = int(yes_no)  
              print (30 * '-')
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
  
    try:
      value = raw_input('How much {0}? (excl. fee) : '.format(trade))
      value = float(value)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
  
    try:
      trailing = raw_input('Trailing percentage? (without %) : ')
      trailing = float(trailing)
    except:
      print '\nInvalid number... going back to Main Menu'
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
      api = bittrex(key, secret)
      values = r.hmget(market, 'Ask', 'MarketName', 'BaseVolume', 'Volume', 'OpenBuyOrders', 'OpenSellOrders', 'High', 'Low', 'Last', 'Bid')
      available = api.getbalance(trade)
      price = float(values[0])
    except:
      print 'API error: Unable to retrieve pricing information... going back to Main Menu'
      time.sleep(1)
      break
    
    if available['Available'] < 0.00100000:
      print (Fore.RED +'Not enough {0} to make a buy... going back to Main Menu'.format(trade))
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
    print 'Proceed?'
    print (Fore.GREEN +'1. yes')
    print (Fore.RED +'2. no')
    try:
      proceed = raw_input('Enter your choice [1-2] : ')
      proceed = int(proceed)
    except:
      print '\nCancelled... going back to Main Menu'
      time.sleep(1)
      break
    if proceed == 1:
      try:
        values = r.hmget(market, 'Ask', 'Bid')
        ask = float(values[0])
        bid = float(values[1])
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
            values = r.hmget(market, 'Ask', 'Bid')
            ask = float(values[0])
            bid = float(values[1])
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
    def start_thread(market, currency, amount, ask, trailing):
      time.sleep(1)
      global messages
      done = False
      thread_name = threading.current_thread().name
      while True:
        try:
          buy = api.buylimit(market, amount, ask)
          time.sleep(0.5)
          buy_uuid = buy['uuid']
          time.sleep(0.5)
          buyorder = api.getorder(uuid=buy_uuid)
          push_send = False
          while buyorder['IsOpen'] == True:
            message = '{0}: Made a buyorder, waiting until it is filled! Remaining: {1:.8f} {2}'.format(thread_name, buyorder['QuantityRemaining'], currency)
            messages[thread_name] = message
            if push_send == False:
              send_pushover(pushover_user, pushover_app, message)
              send_pushbullet(pushbullet_token, message)
              push_send = True
            buyorder = api.getorder(uuid=buy_uuid)
            time.sleep(10)
          trailing_percentage = float(ask) / 100 * float(trailing)
          trailing_stop_loss = float(ask) - float(trailing_percentage)
          stop_loss_percentage = '-{0:.2f}'.format(trailing)
          buyprice = float(ask)
          lastprice = 0
        except:
          message = '{0}: API error: Was unable to create the buyorder... it was cancelled due to:\n{1}'.format(thread_name, buy)
          messages[thread_name] = message
          send_pushover(pushover_user, pushover_app, message)
          send_pushbullet(pushbullet_token, message)
          break
        else:
          while True:
            try:
              time.sleep(0.5)
              values = r.hmget(market, 'Ask')
              ask = float(values[0])
            except:
              message = 'Unable to retrieve data from redis.pontstrader.com, trying to recover...'
              messages[thread_name] = message
            else:
              percentage = 100 * (float(ask) - float(buyprice)) / float(buyprice)
              trailing_percentage = float(ask) / 100 * float(trailing)
              if float(ask) > float(buyprice) and ask != lastprice:
                if float(ask) > lastprice and float(ask) > float(buyprice):
                  new_trailing_stop_loss = float(ask) - float(trailing_percentage)
                  if float(new_trailing_stop_loss) > float(trailing_stop_loss):
                    trailing_stop_loss = float(ask) - float(trailing_percentage)
                    stop_loss_percentage = 100 * (float(trailing_stop_loss) - float(buyprice)) / float(buyprice)
                    message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
                    messages[thread_name] = message
                  else:
                    message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
                    messages[thread_name] = message
                else:
                  message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
                  messages[thread_name] = message
              elif float(ask) < float(buyprice) and float(ask) != float(lastprice):
                message = '{0}: {1} | Buy price {2:.8f} | Price {3:.8f} | Profit: {4:.2f}% | Stop Loss: {5:.8f} ({6:.2f}%)'.format(thread_name, currency, float(buyprice), float(ask), float(percentage), float(trailing_stop_loss), float(stop_loss_percentage))
                messages[thread_name] = message
              elif float(ask) == float(buyprice) and float(ask) != float(lastprice):
                pass
              lastprice = float(ask)
              feepercentage = (0.5*float(buyprice))/100
              buypriceplusfee = float(buyprice) + float(feepercentage)
              if float(ask) <= float(trailing_stop_loss) and float(ask) > float(buypriceplusfee):
                break
          profit_percentage = 100 * (float(trailing_stop_loss) - float(buyprice)) / float(buyprice)
          try:
            sell = api.selllimit(market, amount, trailing_stop_loss)
            sell_uuid = sell['uuid']
            time.sleep(0.5)
            sellorder = api.getorder(uuid=sell_uuid)
            while sellorder['IsOpen'] == True:
              message = '{0}: Stop Loss triggered, waiting until the sell order is completely filled! Remaining: {1:.8f}'.format(thread_name, sellorder['QuantityRemaining'])
              messages[thread_name] = message
              try:
                sellorder = api.getorder(uuid=sell_uuid)
              except:
                pass
              time.sleep(10)
            message = '{0}: {1} SOLD | Buy price {2:.8f} | Sell price {3:.8f} | Profit {4:.2f}% (excl. fee)'.format(thread_name, currency, buyprice, trailing_stop_loss, profit_percentage)
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
        if done == True:
          break
    try:
      datetime = datetime.now().strftime("%d-%m-%Y.%H:%M:%S") 
      threadname = 'ttp-{0}'.format(datetime)
      thread = threading.Thread(name=threadname, target=start_thread,args=(market, currency, amount, ask, trailing))
      thread.daemon = True
      thread.start()
      print (Fore.GREEN +'Made a buy order, to check its status go to the Trailing Stop Loss menu again... going back to Main Menu in 2 seconds')
      time.sleep(2)
    except:
      print (Fore.RED +'Unable to start thread... there is something wrong please contact p0nts!')
