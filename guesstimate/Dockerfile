FROM pytorch/pytorch:latest
#FROM ubuntu:22.04

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y xinetd python3 python3-pip \
    && apt-get clean \
     && rm -rf /var/lib/apt/lists/*
COPY ./flag/flag.txt /tmp/flag.txt
RUN chmod 644 /tmp/flag.txt

RUN useradd -u 31337 -ms /bin/bash challenge
# Prevents the user from writing to the home directory
# RUN chown root:root /home/challenge
# RUN chmod 755 /home/challenge

WORKDIR /home/challenge
# Source files
COPY src src

# Read-only files
COPY ro ro

# Writeable files (in this case, the cache)
COPY rw rw
RUN chown -R challenge:challenge /home/challenge/rw

# Makes the rw directory writeable
RUN chmod 755 /home/challenge/rw

# Install the service
RUN mv src/xinetd.conf /etc/xinetd.d/guesstimate

# Creates the application
COPY src/serve.sh ro/serve.sh
RUN chmod 755 ro/serve.sh
COPY src/guesstimate.py ro/guesstimate.py

# Makes the ro directory read-only
RUN chmod 555 /home/challenge/ro

# Install the requirements
USER challenge
RUN pip3 install -r src/requirements.txt

# Downloads the models and caches them in rw/cache
RUN ./src/init.sh

# The port this leaves on
EXPOSE 15151
CMD ["/usr/sbin/xinetd", "-dontfork"]
