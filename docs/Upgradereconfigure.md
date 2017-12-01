# Upgrade pontstrader
- Download the latest version: https://github.com/p0nt/pontstrader/archive/master.zip
- Or clone it: git clone https://github.com/p0nt/pontstrader.git
- For development branch use: https://github.com/p0nt/pontstrader/archive/development.zip
- Or clone it: git clone -b development https://github.com/p0nt/pontstrader.git

If you would like to upgrade your old version towards a newer version, here is a small how to:
  - Download and unzip the new version
  - Remove the functions directory together with run.py in the root directory of the script, the path where you installed pontstrader (!!! Make sure not to remove config.json, unless you want to redo the installation wizard)
  - Done, you can run pontstrader as you normally do (The version will show at the top from version 3.2 and above)
  
# Re-configure pontstrader

Remove config.json in the parent directory to make this happen, re-run pontstrader to start the installation wizard again.
