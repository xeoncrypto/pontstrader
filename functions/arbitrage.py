#!/usr/bin/env python
  
def arbitrage(redis_password):
  
  import time, json, sys, requests, operator, threading, redis
  from pprint import pprint
  from time import gmtime, strftime
  from colorama import Fore, Back, Style, init
  init(autoreset=True)
  try:
    r_bittrex = redis.Redis(host='redis.pontstrader.com', port=6380, db=0, password=redis_password)
    r_hitbtc = redis.Redis(host='redis.pontstrader.com', port=6380, db=1, password=redis_password)
  except:
    print 'Unable to connect to redis.pontstrader.com, trying redis2.pontstrader.com...'
    try:
      r_bittrex = redis.Redis(host='redis2.pontstrader.com', port=6380, db=0, password=redis_password)
      r_hitbtc = redis.Redis(host='redis2.pontstrader.com', port=6380, db=1, password=redis_password)
    except:
      print 'Unable to connect to redis2.pontstrader.com... I am sorry but you can not continue now, please contact p0nts!'
  
  while True:
    def apiconnect():
      global hitbtc_api
      global hitbtc_ticker
      global polo_api
      global binance_api
      global bitfinex_api
  
    def retrieve_pricing():

      global count
      count = 0
  
      try:
        hitbtc_api = requests.get('https://api.hitbtc.com/api/2/public/symbol')
        hitbtc_ticker = requests.get('https://api.hitbtc.com/api/2/public/ticker')
      except:
        print 'HitBTC API error: {0}'.format(hitbtc_api)
      try:
        polo_api = requests.get('https://poloniex.com/public?command=returnTicker')
      except:
        print 'Poloniex API error: {0}'.format(polo_api)
      try:
        binance_api = requests.get('https://www.binance.com/api/v1/ticker/allBookTickers')
      except:
        print 'Poloniex API error: {0}'.format(binance_api)
      try:
        bitfinex_api = requests.get('https://api.bitfinex.com/v1/symbols')
      except:
        print 'Bitfinex API error: {0}'.format(bitfinex_api)
  
      global bittrex_markets
      global hitbtc_markets
      global polo_markets
      global binance_markets
      global bitfinex_markets
      global bitfinex_markets2
      global bittrex_bid
      global bittrex_ask
      global hitbtc_bid
      global hitbtc_ask
      global polo_bid
      global polo_ask
      global binance_bid
      global binance_ask
      global bitfinex_bid
      global bitfinex_ask
      global sort_percentage
  
      bittrex_markets = []
      hitbtc_markets = []
      polo_markets = []
      binance_markets = []
      bitfinex_markets = []
      bitfinex_markets2 = []
      bittrex_bid = {}
      bittrex_ask = {}
      hitbtc_bid = {}
      hitbtc_ask = {}
      polo_bid = {}
      polo_ask = {}
      binance_bid = {}
      binance_ask = {}
      bitfinex_bid = {}
      bitfinex_ask = {}
      sort_percentage = []
  
      keys = r_bittrex.keys()
      for key in r_bittrex.scan_iter():
        bittrex_markets.append(key)
        values = r_bittrex.hmget(key, 'Ask', 'Bid')
        ask = values[0]
        bid = values[1]
        try:
          float(bid)
        except:
          pass
        else:
          if float(bid) > 0:
            bittrex_bid[key]=bid
        try:
          float(ask)
        except:
          pass
        else:
          if float(ask) > 0:
            bittrex_ask[key]=ask

      for coin in hitbtc_api.json():
        if coin['baseCurrency'] == 'DSH':
          pass
        elif coin['baseCurrency'] == 'BCC':
          pass
        else:
          hitbtc_base = coin['quoteCurrency'].replace("USD", "USDT")
          hitbtc_currency = coin['baseCurrency']
          hitbtc = '{0}-{1}'.format(hitbtc_base, hitbtc_currency)
          hitbtc_markets.append(hitbtc)
          symbol = '{0}{1}'.format(coin['baseCurrency'], coin['quoteCurrency'])
          for ticker in hitbtc_ticker.json():
            if ticker['symbol'] == symbol:
              try:
                float(ticker['bid'])
              except:
                pass
              else:
                if float(ticker['bid']) > 0:
                  hitbtc_bid[hitbtc]=ticker['bid']
              try:
                float(ticker['ask'])
              except:
                pass
              else:
                if float(ticker['ask']) > 0:
                  hitbtc_ask[hitbtc]=ticker['ask']
      for coin in polo_api.json():
        if coin.endswith('bcc'):
          pass
        else:
          polo = coin.replace("_", "-")
          polo_markets.append(polo)
          try:
            float(polo_api.json()[coin]['highestBid'])
          except:
            pass
          else:
            if float(polo_api.json()[coin]['highestBid']) > 0:
              polo_bid[polo]=polo_api.json()[coin]['highestBid']
          try:
            float(polo_api.json()[coin]['lowestAsk'])
          except:
            pass
          else:
            if float(polo_api.json()[coin]['lowestAsk']) > 0: 
              polo_ask[polo]=polo_api.json()[coin]['lowestAsk']
  
      for coin in binance_api.json():
        binance = coin['symbol']
        if binance.startswith('ETC'):
          pass
        elif binance.startswith('BCC'):
          pass
        elif binance.endswith('BTC'):
          binance_currency = binance.rsplit('BTC', 1)[0]
          binance_base = 'BTC'
          binance = '{0}-{1}'.format(binance_base, binance_currency)
          binance_markets.append(binance)
          try:
            float(coin['bidPrice'])
          except:
            pass
          else:
            if float(coin['bidPrice']) > 0:
              binance_bid[binance]=coin['bidPrice']
          try:
            float(coin['askPrice'])
          except:
            pass
          else:
            if float(coin['askPrice']) > 0:
              binance_ask[binance]=coin['askPrice']
        elif binance.endswith('ETH'):
          binance_currency = binance.rsplit('ETH', 1)[0]
          binance_base = 'ETH'
          binance = '{0}-{1}'.format(binance_base, binance_currency)
          binance_markets.append(binance)
          try:
            float(coin['bidPrice'])
          except:
            pass
          else:
            if float(coin['bidPrice']) > 0:
              binance_bid[binance]=coin['bidPrice']
          try:
            float(coin['askPrice'])
          except:
            pass
          else:
            if float(coin['askPrice']) > 0:
              binance_ask[binance]=coin['askPrice']
        elif binance.endswith('USDT'):
          binance_currency = binance.rsplit('USDT', 1)[0]
          binance_base = 'USDT'
          binance = '{0}-{1}'.format(binance_base, binance_currency)
          binance_markets.append(binance)
          try:
            float(coin['bidPrice'])
          except:
            pass
          else:
            if float(coin['bidPrice']) > 0:
              binance_bid[binance]=coin['bidPrice']
          try:
            float(coin['askPrice'])
          except:
            pass
          else:
            if float(coin['askPrice']) > 0:
              binance_ask[binance]=coin['askPrice']
  
      for coin in bitfinex_api.json():
        if coin.startswith('dsh'):
          pass
        elif coin.startswith('bcc'):
          pass
        elif coin.endswith('btc'):
          bitfinex_currency = coin.rsplit('btc', 1)[0]
          bitfinex_base = 'BTC'
          bitfinex = 't{1}{0}'.format(bitfinex_base.upper(), bitfinex_currency.upper())
          bitfinex2 = '{0}-{1}'.format(bitfinex_base.upper(), bitfinex_currency.upper())
          bitfinex_markets.append(bitfinex)
          bitfinex_markets2.append(bitfinex2)
        elif coin.endswith('eth'):
          bitfinex_currency = coin.rsplit('eth', 1)[0]
          bitfinex_base = 'ETH'
          bitfinex = 't{1}{0}'.format(bitfinex_base.upper(), bitfinex_currency.upper())
          bitfinex2 = '{0}-{1}'.format(bitfinex_base.upper(), bitfinex_currency.upper())
          bitfinex_markets.append(bitfinex)
          bitfinex_markets2.append(bitfinex2)
        elif coin.endswith('usd'):
          bitfinex_currency = coin.rsplit('usd', 1)[0]
          bitfinex_base = 'USD'
          bitfinex_base2 = 'USDT'
          bitfinex = 't{1}{0}'.format(bitfinex_base.upper(), bitfinex_currency.upper())
          bitfinex2 = '{0}-{1}'.format(bitfinex_base2.upper(), bitfinex_currency.upper())
          bitfinex_markets.append(bitfinex)
          bitfinex_markets2.append(bitfinex2)
      coins = ",".join(bitfinex_markets)
      try:
        url = 'https://api.bitfinex.com/v2/tickers?symbols={0}'.format(coins)
        bitfinex_symbols = requests.get(url)
      except:
        print 'Bitfinex API error: {0}'.format(bitfinex_symbols)
      for coin in bitfinex_symbols.json():
        if coin[0].endswith('BTC'):
          bitfinex_currency = coin[0].rsplit('BTC', 1)[0][1:]
          bitfinex_base = 'BTC'
        elif coin[0].endswith('ETH'):
          bitfinex_currency = coin[0].rsplit('ETH', 1)[0][1:]
          bitfinex_base = 'ETH'
        elif coin[0].endswith('USD'):
          bitfinex_currency = coin[0].rsplit('USD', 1)[0][1:]
          bitfinex_base = 'USDT'
        bitfinex = '{0}-{1}'.format(bitfinex_base.upper(), bitfinex_currency.upper())
        try:
          float(coin[1])
        except:
          pass
        else:
          if float(coin[1]) > 0:
            bitfinex_bid[bitfinex]=coin[1]
        try:
          float(coin[3])
        except:
          pass
        else:
          if float(coin[3]) > 0:
            bitfinex_ask[bitfinex]=coin[3]
      count += 1
  
    thread = threading.Thread(name=arbitrage, target=retrieve_pricing)
    thread.daemon = True
    thread.start()
  
    def hitbtc():
      if coin in hitbtc_bid:
        if market == 'BTC':
          if coin.startswith('BTC'):
            bid = float(hitbtc_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'ETH':
          if coin.startswith('ETH'):
            bid = float(hitbtc_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'USDT':
          if coin.startswith('USDT'):
            bid = float(hitbtc_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'All':
          bid = float(hitbtc_bid[coin])
          percentage = 100 * (float(bid) - float(ask)) / float(ask)
          add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
          sort_percentage.append(dict(add_dict))
  
    def poloniex():
      if coin in polo_bid:
        if market == 'BTC':
          if coin.startswith('BTC'):
            bid = float(polo_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'ETH':
          if coin.startswith('ETH'):
            bid = float(polo_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'USDT':
          if coin.startswith('USDT'):
            bid = float(polo_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'All':
          bid = float(polo_bid[coin])
          percentage = 100 * (float(bid) - float(ask)) / float(ask)
          add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
          sort_percentage.append(dict(add_dict))
  
    def bittrex():
      if coin in bittrex_bid:
        if market == 'BTC':
          if coin.startswith('BTC'):
            bid = float(bittrex_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'ETH':
          if coin.startswith('ETH'):
            bid = float(bittrex_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'USDT':
          if coin.startswith('USDT'):
            bid = float(bittrex_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'All':
          bid = float(bittrex_bid[coin])
          percentage = 100 * (float(bid) - float(ask)) / float(ask)
          add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
          sort_percentage.append(dict(add_dict))
  
    def binance():
      if coin in binance_bid:
        if market == 'BTC':
          if coin.startswith('BTC'):
            bid = float(binance_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'ETH':
          if coin.startswith('ETH'):
            bid = float(binance_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'USDT':
          if coin.startswith('USDT'):
            bid = float(binance_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'All':
          bid = float(binance_bid[coin])
          percentage = 100 * (float(bid) - float(ask)) / float(ask)
          add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
          sort_percentage.append(dict(add_dict))
  
    def bitfinex():
      if coin in bitfinex_bid:
        if market == 'BTC':
          if coin.startswith('BTC'):
            bid = float(bitfinex_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'ETH':
          if coin.startswith('ETH'):
            bid = float(bitfinex_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'USDT':
          if coin.startswith('USDT'):
            bid = float(bitfinex_bid[coin])
            percentage = 100 * (float(bid) - float(ask)) / float(ask)
            add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
            sort_percentage.append(dict(add_dict))
        elif market == 'All':
          bid = float(bitfinex_bid[coin])
          percentage = 100 * (float(bid) - float(ask)) / float(ask)
          add_dict = {'market': coin, 'from': frm, 'to':to, 'ask': ask, 'bid': bid, 'percentage': percentage}
          sort_percentage.append(dict(add_dict))
  
    print (30 * '-')
    print(Fore.GREEN +'   A R B I T R A G E')
    print (30 * '-')
    print ('From what Exchange?')
    print(Fore.YELLOW +'1. Bittrex')
    print(Fore.YELLOW +'2. HitBTC')
    print(Fore.YELLOW +'3. Poloniex')
    print(Fore.YELLOW +'4. Binance')
    print(Fore.YELLOW +'5. Bitfinex')
    print(Fore.GREEN +'6. All')
    print(Fore.RED +'7. Back to Main Menu')
    try:
      choice = raw_input('Enter your choice [1-7] : ')
      print (30 * '-')
      choice = int(choice)
      if choice == 1:
        exchange = 'Bittrex'
      elif choice == 2:
        exchange = 'HitBTC'
      elif choice == 3:
        exchange = 'Poloniex'
      elif choice == 4:
        exchange = 'Binance'
      elif choice == 5:
        exchange = 'Bitfinex'
      elif choice == 6:
        exchange = 'All'
      elif choice == 7:
        print 'Going back to Main Menu'
        break
    except:
      print 'ERROR: Please select a number!'
      break
    print ('What Market?')
    print(Fore.YELLOW +'1. BTC')
    print(Fore.YELLOW +'2. ETH')
    print(Fore.YELLOW +'3. USDT')
    print(Fore.GREEN +'4. All')
    print(Fore.RED +'5. Exit to Main Menu')
    try:
      market = raw_input('Enter your choice [1-5] : ')
      print (30 * '-')
      market = int(market)
      if market == 1:
        market = 'BTC'
      elif market == 2:
        market = 'ETH'
      elif market == 3:
        market = 'USDT'
      elif market == 4:
        market = 'All'
      elif market == 5:
        print 'Going back to Main Menu'
        break
    except:
      print 'ERROR: Please select a number!'
      break
    try:
      percentage = raw_input('Show from x percentage profit (decimals allowed)? [0-1000] : ')
      print (30 * '-')
      percentage = float(percentage)
    except:
      print 'ERROR: Please select a number!'
      break
  
    while True:
      while count == 0:
        print(Fore.YELLOW +'Retrieving pricing data from several API\'s, please wait...')
        time.sleep(2)
      if exchange == 'Bittrex':
        frm = 'Bitt'
        for coin in bittrex_markets:
          try:
            ask = float(bittrex_ask[coin])
          except:
            pass
          if coin in hitbtc_markets:
            to = 'Hitb'
            hitbtc()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in binance_markets:
            to = 'Bina'
            binance()
          if coin in bitfinex_markets2:
            to = 'Bitf'
            bitfinex()
        sort_percentage.sort(key=operator.itemgetter('percentage'))
        number = 0
        for entry in sort_percentage:
          if entry['percentage'] > 1000:
            pass
          elif entry['percentage'] > percentage:
            number += 1
            if len(entry['market']) == 6 or len(entry['market']) == 7:
              print '{6}.\t{0}\t\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
            else:
              print '{6}.\t{0}\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
  
      elif exchange == 'HitBTC':
        frm = 'Hitb'
        for coin in hitbtc_markets:
          try:
            ask = float(hitbtc_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in binance_markets:
            to = 'Bina'
            binance()
          if coin in bitfinex_markets2:
            to = 'Bitf'
            bitfinex()
        sort_percentage.sort(key=operator.itemgetter('percentage'))
        number = 0
        for entry in sort_percentage:
          if entry['percentage'] > 1000:
            pass
          elif entry['percentage'] > percentage:
            number += 1
            if len(entry['market']) == 6 or len(entry['market']) == 7:
              print '{6}.\t{0}\t\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
            else:
              print '{6}.\t{0}\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
  
      elif exchange == 'Poloniex':
        frm = 'Polo'
        for coin in polo_markets:
          try:
            ask = float(polo_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in hitbtc_markets:
            to = 'HitB'
            hitbtc()
          if coin in binance_markets:
            to = 'Bina'
            binance()
          if coin in bitfinex_markets2:
            to = 'Bitf'
            bitfinex()
        sort_percentage.sort(key=operator.itemgetter('percentage'))
        number = 0
        for entry in sort_percentage:
          if entry['percentage'] > 1000:
            pass
          elif entry['percentage'] > percentage:
            number += 1
            if len(entry['market']) == 6 or len(entry['market']) == 7:
              print '{6}.\t{0}\t\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
            else:
              print '{6}.\t{0}\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
  
      elif exchange == 'Binance':
        frm = 'Bina'
        for coin in binance_markets:
          try:
            ask = float(binance_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in hitbtc_markets:
            to = 'Hitb'
            hitbtc()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in bitfinex_markets2:
            to = 'Bitf'
            bitfinex()
        sort_percentage.sort(key=operator.itemgetter('percentage'))
        number = 0
        for entry in sort_percentage:
          if entry['percentage'] > 1000:
            pass
          elif entry['percentage'] > percentage:
            number += 1
            if len(entry['market']) == 6 or len(entry['market']) == 7:
              print '{6}.\t{0}\t\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
            else:
              print '{6}.\t{0}\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
  
      elif exchange == 'Bitfinex':
        frm = 'Bitf'
        for coin in bitfinex_markets2:
          try:
            ask = float(bitfinex_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in hitbtc_markets:
            to = 'Hitb'
            hitbtc()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in binance_markets:
            to = 'Bina'
            binance()
        sort_percentage.sort(key=operator.itemgetter('percentage'))
        number = 0
        for entry in sort_percentage:
          if entry['percentage'] > 1000:
            pass
          elif entry['percentage'] > percentage:
            number += 1
            if len(entry['market']) == 6 or len(entry['market']) == 7:
              print '{6}.\t{0}\t\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
            else:
              print '{6}.\t{0}\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
  
      elif exchange == 'All':
        frm = 'Bitt'
        for coin in r_bittrex.scan_iter():
          try:
            ask = float(bittrex_ask[coin])
          except:
            pass
          if coin in hitbtc_markets:
            to = 'Hitb'
            hitbtc()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in binance_markets:
            to = 'Bina'
            binance()
        frm = 'Hitb'
        for coin in hitbtc_markets:
          try:
            ask = float(hitbtc_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in binance_markets:
            to = 'Bina'
            binance()
          if coin in bitfinex_markets2:
            to = 'Bitf'
            bitfinex()
        frm = 'Polo'
        for coin in polo_markets:
          try:
            ask = float(polo_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in hitbtc_markets:
            to = 'Hitb'
            hitbtc()
          if coin in binance_markets:
            to = 'Bina'
            binance()
          if coin in bitfinex_markets2:
            to = 'Bitf'
            bitfinex()
        frm = 'Bina'
        for coin in binance_markets:
          try:
            ask = float(binance_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in hitbtc_markets:
            to = 'Hitb'
            hitbtc()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in bitfinex_markets2:
            to = 'Bitf'
            bitfinex()
        frm = 'Bitf'
        for coin in bitfinex_markets2:
          try:
            ask = float(bitfinex_ask[coin])
          except:
            pass
          if coin in bittrex_markets:
            to = 'Bitt'
            bittrex()
          if coin in hitbtc_markets:
            to = 'Hitb'
            hitbtc()
          if coin in polo_markets:
            to = 'Polo'
            poloniex()
          if coin in binance_markets:
            to = 'Bina'
            binance()
        sort_percentage.sort(key=operator.itemgetter('percentage'))
        number = 0
        for entry in sort_percentage:
          if entry['percentage'] > 1000:
            pass
          elif entry['percentage'] > percentage:
            number += 1
            if len(entry['market']) == 6 or len(entry['market']) == 7:
              print '{6}.\t{0}\t\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
            else:
              print '{6}.\t{0}\t{4} ({1:.8f})\t{5} ({2:.8f})\t  {3:.2f} %'.format(entry['market'], entry['ask'], entry['bid'], entry['percentage'], entry['from'], entry['to'], number)
      elif choice == 6:
        break
      if number == 0:
        print (Fore.YELLOW +'None found that match your criteria')
      output = (Fore.YELLOW +'Refresh: r+enter | Return to Arbitrage Menu: q+enter : ')
      refresh = raw_input(output)
      refresh = str(refresh)
      if refresh == 'r':
        print (Fore.GREEN +'Ok, refreshing in 15 seconds... (to prevent spam)')
        time.sleep(15)
      elif refresh == 'q':
        break
      else:
        print 'Invalid input, refreshing in 15 seconds... (to prevent spam)'
        time.sleep(15)
      try:
        retrieve_pricing()
      except:
        break
    else:
      print 'ERROR: Invalid number!'
      break
