#!/bin/bash

timeout 180 /home/challenge/src/rate_limiting_client.py --host "192.35.222.130" --challenge ai_pi_escape &&
timeout 180 /home/challenge/src/aipi_escape.py
