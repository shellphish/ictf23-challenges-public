#!/bin/bash

export TERM=xterm
export FLAG=$(cat /flag.txt)
/home/challenge/src/aimazing.py --flag $FLAG 2>&1