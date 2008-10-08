#!/bin/sh
#
# initial-setup.sh - for amat

sudo addgroup jailbird
sudo mkdir -p /jail/skel /jail/home
paster setup-app development.ini
echo "Done."
