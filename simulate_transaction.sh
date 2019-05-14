#!/usr/bin/env bash

data=$(cat txn_example.txt)
cd src
echo "$data" | python3 dumb_user.py