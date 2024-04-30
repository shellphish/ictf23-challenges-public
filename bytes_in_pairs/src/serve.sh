#!/bin/sh
socat \
    -dd \
    -T60 \
    TCP-LISTEN:25932,reuseaddr,fork \
    EXEC:"timeout 60 ./chall.py"
