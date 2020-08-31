#!/bin/bash
if [ $UID != "0" ]; then
  echo "This script must be run as root to run on a workstation"
  exit 1
fi

COMMAND="https-everywhere-standalone --transparent"

./pre-mitm.sh
if id -u httpse > /dev/null 2> /dev/null; then
  sudo -u httpse /var/lib/httpse/$COMMAND
else
  dist/$COMMAND
fi
./post-mitm.sh
