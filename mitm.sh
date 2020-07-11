#!/bin/bash
./pre-mitm.sh
sudo -u mitmproxy mitmproxy --mode transparent -s ./script.py
./post-mitm.sh
