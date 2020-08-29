#!/bin/bash
# Pasyans install script - Harrison Whitner - 08/28/20

pip3 install termcolor                                   # install a necessary package for colored text in the shell

sudo cp pasyans.py -t /usr/local/bin/                    # copy python script to install dir
sudo chmod 755 /usr/local/bin/pasyans.py                 # change the perms for the script
sudo mv /usr/local/bin/pasyans.py /usr/local/bin/pasyans # rename the script to remove the extension
