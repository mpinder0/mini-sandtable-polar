#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

# sleep a bit to allow network to connect
sleep 30
ping github.com -c 5

# start the platter script in venv
cd /home/<user>/Repos/mini-sandtable-polar
sudo -u <user> git pull
. .venv/bin/activate
cd src
python main.py
