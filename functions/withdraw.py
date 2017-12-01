#!/usr/bin/env python
  
def withdraw(key, secret):
  
  import time, json, sys
  from pprint import pprint
  from time import gmtime, strftime
  from bittrex import bittrex
  from colorama import Fore, Back, Style, init
  init(autoreset=True)
  
  while True:
    try:
      api = bittrex(key, secret)
      currencies = api.getcurrencies()
    except:
      print 'Bittrex API error: {0}'.format(api)
  
    print (30 * '-')
    print(Fore.GREEN +'   W I T H D R A W')
    print (30 * '-')
    print(Fore.YELLOW +'NOTE: Make sure Withdraw is allowed for this API key')
    print (30 * '-')
    try:
      balances = api.getbalances()
      print(Fore.GREEN +'Currency\tAvailable')
      number = 0
      list = []
      for coin in balances:
        available = coin["Available"]
        currency = coin["Currency"]
        if available != 0.0:
          number += 1
          list.append(currency)
          if len(currency) > 4:
            print '{0}. {1}\t{2:.8f}'.format(number, currency, available)
          else:
            print '{0}. {1}\t\t{2:.8f}'.format(number, currency, available)
    except:
      print 'Bittrex API error: {0}'.format(balances)
      print 'Going back to Main Menu'
      time.sleep(2)
    try:
      choose_num = raw_input('Enter your choice [1-{0}] : '.format(number))
      choose_num = int(choose_num)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    try:
      choose_num = choose_num - 1
      if choose_num == -1:
        print 'Invalid number... going back to Main Menu'
        time.sleep(1)
        break
      for f in currencies:
        if f['Currency'] == list[choose_num]:
          fee = f['TxFee']
      print(Fore.GREEN +'Starting withdraw for {0}'.format(list[choose_num]))
      print (30 * '-')
      balance = api.getbalance(list[choose_num])
      available = balance["Available"]
      print 'Available: {0} {1}'.format(available, list[choose_num])
      print 'Fee:       {0} {1}'.format(fee, list[choose_num])
      print(Fore.YELLOW +'Fee will be calculated at the end, you may just withdraw the full amount.')
      print (30 * '-')
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    try:
      quantity = raw_input('Quantity? : ')
      quantity = float(quantity)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    if quantity > available:
      print 'You can\'t withdraw more than available. Cancelled...'
      time.sleep(1)
      break
    try:
      address = raw_input('Withdraw Address? : ')
      address = str(address)
    except:
      print 'Invalid input. Cancelled...'
      time.sleep(1)
      break
    try:
      paymentid = raw_input('Payment ID?' + Fore.YELLOW +' (If not required, leave empty)' + Fore.WHITE +' : ')
      paymentid = str(paymentid)
    except:
      print 'Invalid input. Cancelled...'
      time.sleep(1)
      break
    print (30 * '-')
    print(Fore.YELLOW +'BITTREX NOTE: Please verify your withdrawal address. We cannot refund an incorrect withdrawal.')
    print (30 * '-')
    if len(paymentid) > 0:
      print(Fore.GREEN +'You are about to withdraw {0:.8f} {1} to {2} with Payment ID {3}, is this correct?'.format(quantity, list[choose_num], address, paymentid))
    else:
      print(Fore.GREEN +'You are about to withdraw {0:.8f} {1} to {2}, is this correct?'.format(quantity, list[choose_num], address))
    print(Fore.GREEN +'1. yes')
    print(Fore.RED +'2. no (Back to Main Menu)')
    print (30 * '-')
    try:
      yes_no = raw_input('Enter your choice [1-2] : ')
      yes_no = int(yes_no)
    except:
      print '\nInvalid number... going back to Main Menu'
      time.sleep(1)
      break
    if yes_no == 1:
      try:
        if len(paymentid) > 0:
          apicall = api.withdraw(currency=list[choose_num], quantity=quantity, address=address, paymentid=paymentid)
        else:
          apicall = api.withdraw(currency=list[choose_num], quantity=quantity, address=address)
        print apicall['uuid']
        after_fee = quantity - fee
        if len(paymentid) > 0:
          print(Fore.GREEN +'Added a withdraw order for {0:.8f} {1} towards {2} with Payment ID {3} (incl. bittrex fee)'.format(after_fee, list[choose_num], address, paymentid))
        else:
          print(Fore.GREEN +'Added a withdraw order for {0:.8f} {1} towards {2} (incl. bittrex fee)'.format(after_fee, list[choose_num], address))
        print 'Returning to Main Menu in 5 seconds...'
        time.sleep(5)
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
