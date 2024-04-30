#!/bin/sh

timeout -k1 100 stdbuf -i0 -o0 -e0 /rustyneurone 2>/dev/null; sleep 1
