#!/bin/sh
# launcher.sh
#
# add to cron with
# crontab -e
# and add the following line:
# @reboot sh /home/<user>/launcher.sh >/home/<user>/logs/cronlog 2>&1

# sleep a bit to allow network to connect
sleep 30
ping github.com -c 5

# start the plotter script in venv
cd /home/<user>/Repos/mini-sandtable-polar
# make sure the git repo is up to date
sudo -u <user> git pull
# activate the virtual environment
. .venv/bin/activate
cd src
# run the script
python main.py
