#!/usr/bin/env bash

block=$(cat block0.json)
cd src
echo "$block" | python3 dumb_send.py
