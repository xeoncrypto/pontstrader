#!/usr/bin/env python

def watch(key, secret, redis_password):

  import time, json, sys, threading, redis
  from pprint import pprint
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

  class TestThread(threading.Thread):
    def __init__(self, name='Watch'):
      self._stopevent = threading.Event( )
      self._sleepperiod = 1.0
      threading.Thread.__init__(self, name=name)
    def run(self):
      print(Fore.GREEN +'Starting watch for {0}'.format(market))
      print(Fore.YELLOW +'Checked every 0.5 seconds, only price/percentage changes will be shown')
      print(Fore.YELLOW +'Price/Percentage changes are based on the moment the watch is started')
      print(Fore.YELLOW +'Please note the Timestamp is taken from Bittrex, can be different then yours')
      print(Fore.RED +'q+enter to return to Main Menu')
      lastprice = '0'
      try:
        values = r.hmget(market, 'Ask')
        start_price = float(values[0])
      except:
        print 'Unable to retrieve data from redis.pontstrader.com'
      else:
        while not self._stopevent.isSet( ):
          try:
            values = r.hmget(market, 'Ask', 'TimeStamp')
            price = float(values[0])
            timestamp = values[1]
          except:
            print (Fore.RED +'Unable to retrieve data from redis.pontstrader.com, trying to recover...')
          else:
            percent = 100 * (float(price) - float(start_price)) / float(start_price)
            if price != lastprice:
              if percent < 0.00:
                print ('{0} - The {1} price for 1 {2} is {3:.8f} {4}'.format(timestamp, trade, currency, price, trade) + (Fore.RED + ' ({0:.2f})%'.format(percent)))
                lastprice = price
              elif percent > 0.00:
                print ('{0} - The {1} price for 1 {2} is {3:.8f} {4}'.format(timestamp, trade, currency, price, trade) + (Fore.GREEN + ' ({0:.2f})%'.format(percent)))
                lastprice = price
              else:
                print '{0} - The {1} price for 1 {2} is {3:.8f} {4} ({5:.2f}%)'.format(timestamp, trade, currency, price, trade, percent)
                lastprice = price
            time.sleep(0.5)
          self._stopevent.wait(self._sleepperiod)
        print "Returning to Main Menu"
    def join(self, timeout=None):
        self._stopevent.set( )
        threading.Thread.join(self, timeout)

  if __name__ == "watch":
    proceed = False
    while True:
      print (30 * '-')
      print(Fore.GREEN +'   W A T C H')
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
        proceed = False
        break
      if trade == 1:
        trade = 'BTC'
      elif trade == 2:
        trade = 'ETH'
      elif trade == 3:
        trade = 'USDT'
      elif trade == 4:
        proceed = False
        break
      else:
        print '\nInvalid number... going back to Main Menu'
        time.sleep(1)
        proceed = False
        break
      currency = raw_input('Currency? (examples: LTC / NEO / OMG) : ').upper()
      market = '{0}-{1}'.format(trade, currency)
      proceed = True
      break

    if proceed == True:
      testthread = TestThread()
      testthread.start()
      while True:
        exit = raw_input((Fore.RED +'\nq+enter to return to Main Menu\n'))
        if exit == 'q':
          testthread.join()
          break
