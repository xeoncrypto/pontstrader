# v3.1
- Arbitrage hot fix (float error)

v3
- Removed the automated watch function, now allows quiting during watch again
- All public API data is now retrieved from the pontstrader servers taken from a Redis cluster, allowing more speed, less limitations and flexibility for extra functions in the future
- Allot of things done in the background such as:
* Monitoring (collect, visualize, notify)
* Infrastructure (server migration make it ready for Redis)
* Backup (snapshots and backups)
* Security (firewalls)
* Allot other small stuff

v2.2
- Added refresh option after checking trailing stop loss status
- Revamped the progress output on the trailing stop function, its now possible the check all status updates
v2.1
- Retrieving public market data for any function now runs in the background which improves speed even more
- Fixed error output for Pushover and Pushbullet
- Removed usage of CTRL-C in the script

v2.0 (With trailing stop trading BETA)
- New trading function: Trailing Stop for Bittrex (check the docs for more information)
- New feature: Push notifications on your phone with Pushover or Pushbullet (Trailing stop function)
- Arbitrage function out of BETA - Arbitrage speed improvements, data retrieving is now running in the background
- Removed exit's (BETA) on the arbitrage function, script does not exit anymore
- Fixed a bug where closing the function would give a API error
- Fixed a bug which made the script crash if you had no orders in the orderbook
- Fixed a bug where the arbitrage function would crash if you use the menu to quick
- Fixed a error caused by choosing 0 in the sell, orderbook and withdraw function
- Watch function is not killed on API error anymore during watch
- Arbitrage function is not killed on API error anymore during watch
- Added function to buy/sell and buysell that will allow a watch after the order to see if its filled
- Added missing BTC value for the BTC currency in the balance function

v1.20 (With arbitrage BETA)
- Version check (e.g. run.py version)
- Cancelling a watch allows you to quickly watch a new coin
- Removed all sys.exit's which means the script only dies in API errors or invalid input now
- Added back to Main Menu options
- Removal of unrealistic arbitrage oppertunaties (1000% +)
- Balance gets automatically refreshed every 30 seconds
- Fixed arbitrage polo zero float error (Thanks Robbert)

v1.14 (With arbitrage BETA)
- Added option to choose market with arbitrage
- Added option to choose from how many percentage you want entries to show

v1.13 (With arbitrage BETA)
- Added bitfinex to the arbitrage function

v1.12
- Withdraw function release

v1.11 BETA (With arbitrage and withdraw BETA)
- Arbitrage results now have numbers for future usage (automation)
- Withdraw function now allows the use of payment ID's

v1.1 BETA
- Arbitrage BETA
- Withdraw BETA (does not work with Payment ID's yet)
- Buy / Watch / Sell: Fixed error when using lowercase characters as currency
- Arbitrage: Added support for Binance
- Colors: Removed the ansicon requirement for windows (python-colorama)
- Added an install wizard when the script is used for the first time

v1.0
- Public release

v0.9
- Balance: Balance now shows total estimated value in BTC and Dollar
- Balance: You can now choose out of the 3 possible Bittrex markets instead of typing them

v0.8
- Balance / Sell: Added more information during a buy or sell, price/fee/minimum etc.

- Orderbook: Open orders menu option to allow overview and removal of open orders
v0.7
- Buy / Sell functions revamped
- Buy and Sell with custom values instead of only Last price
- Sell directly from your wallet, instead of manually inserting currency to sell (after all, you can only sell what you own right?)

v0.6
- NEW: Balance function

v0.5
- NEW: Orderbook

v0.4
- NEW: Watch function

v0.3
- NEW: Buy + Sell funtion

v0.2
- NEW: Sell function

v0.1
- NEW: Buy function
