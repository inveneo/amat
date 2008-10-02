#!/bin/sh
#
# initial-setup.sh - for amat

sudo addgroup jailbird
sudo mkdir -p /jail/skel
paster setup-app development.ini
echo "Done."
