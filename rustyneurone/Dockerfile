FROM ubuntu:22.04

run apt-get -qq update
run apt-get install -qq --no-install-recommends xinetd rsyslog software-properties-common
run apt-get install -y netcat-traditional htop expect

run chmod o-w /var/tmp
run chmod o-w /dev/shm

copy src/flag.txt /flag.txt
copy src/xinetd.conf /xinetd.conf
copy src/wrapper.sh /wrapper.sh
copy src/rustyneurone /rustyneurone

run chmod +x /rustyneurone
run chmod +x /wrapper.sh

expose 3427
cmd ["/usr/sbin/xinetd", "-syslog", "local0", "-dontfork", "-f", "/xinetd.conf"]

