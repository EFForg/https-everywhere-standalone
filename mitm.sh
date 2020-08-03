#!/bin/bash
./pre-mitm.sh
python https-everywhere-mitmproxy.py --transparent
./post-mitm.sh
