#!/bin/bash

timeout 180 /home/challenge/src/rate_limiting_client.py --host "192.35.222.130" --challenge ci_ninja2 &&
timeout 180 /home/challenge/src/ci_ninja2.py
