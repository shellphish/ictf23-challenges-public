#! /bin/bash

rm ./rustyneurone
rm target/debug/rustyneurone

cargo build

cp target/debug/rustyneurone .

strip -g -S -d --strip-debug ./rustyneurone

