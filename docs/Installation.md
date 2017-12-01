# Installation Guide

#### 1. Install python 2.7
  - Windows & Mac: https://www.python.org/downloads/release/python-2714/
  - Linux: apt-get install python2.7 / yum install python2.7

#### 2. Install python-pip:
  - Windows: https://pip.pypa.io/en/stable/installing/
  - Linux: apt-get install python-pip / yum install python-pip
  - Mac:
  ```
  easy_install pip
  ```

#### 3. Install python-requests
  - Windows (This only works when you've successfully installed python-pip):
  ```
  C:\Python27\python.exe -m pip install requests
  ```
  - Linux:
  ```
  apt-get install python-requests / yum install python-requests
  ```
  - Mac:
  ```
  python -m pip install requests
  or
  easy_install request
  ```

#### 4. Install python-colorama for colors:
  - Windows: https://pypi.python.org/pypi/colorama/0.2.7#downloads
  - Linux:
  ```
  apt-get install python-colorama / yum install python-colorama
  ```
  - Mac:
  ```
  python <pathtocolorama>/setup.py install
  or
  easy_install colorama
  ```
  
#### 5. Install python-redis
  - Windows:
  ```
  C:\Python27\python.exe -m pip install redis
  ```
  Linux: 
  ```
  pip install redis
  ```
  Mac:
  ```
  pip install redis
  or
  easy_install redis
  ```

#### 6. Download the script
  - Download the latest version: https://github.com/p0nt/pontstrader/archive/master.zip
  - Or clone it:
  ```
  git clone https://github.com/p0nt/pontstrader.git
  ```
  - For development branch use: https://github.com/p0nt/pontstrader/archive/development.zip
  - Or clone it:
  ```
  git clone -b development https://github.com/p0nt/pontstrader.git
  ```

#### 7. Now you will be able to run the script
  - Windows: run cmd as administrator, cd to the right directory, run: python run.py
  - Linux & Mac: cd to the pontstrader directory and run: ./run.py
  - For windows you can also make a .bat file:
  ```
    --- BEGIN ---
    @echo off
    TITLE P O N T S T R A D E R
    "C:\Python27\python.exe" C:\Python27\Scripts\run.py
    pause > nul
    --- END ---
  ```

#### 8. Running the script for the first time allows you to setup a few things
  ###### - Bittrex API
  Because you are trading with pontstrader you will have to provide the Bittrex API key and secret during the installation wizard, you can create a key+secret via https://bittrex.com/Manage#sectionApi
  For most of the functions the first 2 slicers need to be on, if you would like to Withdraw with pontstrader please allow the Withdraw slider. In the future we will allow market trading, from that moment the 3th slider should be on as well.
  If you enable Withdraw, make sure to add a IP whitelist for this key which will disallow others to withdraw through your API keys should they ever get known by 3th party. (pontstrader will not send or store your keys anywhere)
  
  ###### - Pushover / Pushbullet
  Since version 2.0 you are able to retrieve pushover or pushbullet messages on your phone uppon changes in certain 24/7 running functions. You can either configure or skip if you dont want.
  More information on: https://www.pushover.com or https://www.pushbullet.com (I would recomment pushover over pushbullet, but it costs a little money so make your own choice)

  ##### - Redis password
  Since version 3.2 pontstrader can be found on Github, therefore the code is public which made me remove the password from the code and added it to the wizard everybody will have to go through starting the script for the first time, this disallows people from using the script without paying 10 dollars for it.
  If you need the password, please contact p0nts on telegram!
