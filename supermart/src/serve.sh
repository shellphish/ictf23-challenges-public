#!/bin/sh
socat \
    -dd \
    -T60 \
    TCP-LISTEN:25931,reuseaddr,fork \
    EXEC:"timeout 60 python3 chall.py"
