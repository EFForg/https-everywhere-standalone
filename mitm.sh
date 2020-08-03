#!/bin/bash
COMMAND="python3 https-everywhere-mitmproxy.py --transparent"

./pre-mitm.sh
if id -u httpse > /dev/null 2> /dev/null; then
  sudo -u httpse $COMMAND
else
  $COMMAND
fi
./post-mitm.sh
