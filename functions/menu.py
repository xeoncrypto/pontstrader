#!/usr/bin/env python

def menu(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password):

  import sys
  import time
  import threading
  import os
  from buy import buy
  from sell import sell
  from buysell import buysell
  from balances import balances
  from orderbook import orderbook
  from watch import watch
  from withdraw import withdraw
  from arbitrage import arbitrage
  from trailing import trailing
  from colorama import Fore, Back, Style, init
  init(autoreset=True)

  while True:
    print (30 * '-')
    print(Fore.GREEN + 'P O N T S T R A D E R . C O M')
    print (30 * '-')
    print(Fore.YELLOW + '1. Buy')
    print(Fore.YELLOW + '2. Sell')
    print(Fore.YELLOW + '3. Buy and Sell')
    print(Fore.YELLOW + '4. Balances')
    print(Fore.YELLOW + '5. Orderbook')
    print(Fore.YELLOW + '6. Watch coin')
    print(Fore.YELLOW + '7. Withdraw')
    print(Fore.YELLOW + '8. Arbitrage')
    print(Fore.YELLOW + '9. Trailing stop (BETA)')
    print(Fore.RED +'10. Exit')
    print (30 * '-')

    try:
      choice = raw_input('Enter your choice [1-10] : ')
      choice = int(choice)
    except:
      print 'Invalid number. Try again...'

    # BUY
    if choice == 1:
      buy(apikey, apisecret, redis_password)

    # SELL
    elif choice == 2:
      sell(apikey, apisecret, redis_password)

    # BUY AND SELL
    elif choice == 3:
      buysell(apikey, apisecret, redis_password)

    # SHOW WALLETS
    elif choice == 4:
      balances(apikey, apisecret, redis_password)

    # OPEN ORDERS
    elif choice == 5:
      orderbook(apikey, apisecret, redis_password)

    # WATCH
    elif choice == 6:
      watch(apikey, apisecret, redis_password)

    # WITHDRAW
    elif choice == 7:
      withdraw(apikey, apisecret)

    # ARBITRAGE
    elif choice == 8:
      arbitrage(redis_password)

    # TRAILING
    elif choice == 9:
      trailing(apikey, apisecret, pushover_user, pushover_app, pushbullet_token, redis_password)

    # EXIT
    elif choice == 10:
      count = threading.activeCount()
      if count > 1:
        threads = threading.enumerate()
        thread_counter = 0
        for t in threading.enumerate():
          if 'arbitrage' in t.name:
            pass
          elif 'Main' in t.name:
            pass
          else:
            thread_counter += 1
        if thread_counter > 0:
          print (Fore.YELLOW +'WARNING: There are currently {0} active trade(s), are you sure you want to exit?'.format(thread_counter))
          print(Fore.GREEN +'1. yes')
          print(Fore.RED +'2. no')
          try:
            yes_no = raw_input('Enter your choice [1-2] : ')
            yes_no = int(yes_no)
          except:
            print 'Invalid number... going back to Main Menu'
          if yes_no == 1:
            print 'Exiting...'
            sys.exit()
          elif yes_no == 2:
            print 'Good... going back to Main Menu'
          else:
            print 'Invalid number... going back to Main Menu'
        else:
          print 'Exiting...'
          sys.exit()
      else:
        print 'Exiting...'
        sys.exit()

    # ELSE EXIT
    else:
      print 'Invalid number. Try again...'
