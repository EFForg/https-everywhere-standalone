#!/bin/bash
./pre-mitm.sh
mitmdump --mode transparent -s ./script.py
./post-mitm.sh
