#!/usr/bin/env bash

block=$(cat blockely.json)
cd src
echo "$block" | python3 dumb_send.py
