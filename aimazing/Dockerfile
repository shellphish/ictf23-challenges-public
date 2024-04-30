FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y socat python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a new user (user=31337 in socat)
RUN useradd -u 31337 -ms /bin/bash challenge
# Prevents the user from writing to the home directory
RUN chown root:root /home/challenge
RUN chmod 755 /home/challenge

# Copy files
COPY ./src/flag.txt /flag.txt
COPY src /home/challenge/src

# Set permissions
RUN chmod 644 /flag.txt
RUN chmod 755 /home/challenge/src/service.sh
RUN chmod 755 /home/challenge/src/aimazing.py

# Install the service
RUN python3 -m pip install -r /home/challenge/src/requirements.txt

# The port this leaves on
EXPOSE 11300
CMD ["socat", "TCP-LISTEN:11300,reuseaddr,fork", "EXEC:'/home/challenge/src/service.sh',pty,raw,echo=0,su=challenge"]

# docker rm -f $(docker ps -a -q --filter ancestor=aimazing_high); docker build -t aimazing_high . && docker run -d -p 11300:11300 aimazing_high
# # stty -icanon && nc localhost 11300