FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y coreutils build-essential socat python3 python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a new user (su=challenge in socat)
RUN useradd -u 31337 -ms /bin/bash challenge
# Prevents the user from writing to the home directory
RUN chown root:root /home/challenge
RUN chmod 755 /home/challenge

# Copy files
COPY ./src/flag.txt /flag.txt
COPY src /home/challenge/src

# Set permissions
RUN chmod 600 /flag.txt
RUN chmod 700 /home/challenge/src/setup.sh
RUN chmod 700 /home/challenge/src/create_chroot.sh
RUN chmod 700 /home/challenge/src/rate_limiting_client.py
RUN chmod 700 /home/challenge/src/ci_ninja2.py
RUN chmod 700 /home/challenge/src/service.sh

# Install the service
WORKDIR /home/challenge/src
RUN /home/challenge/src/create_chroot.sh
RUN /home/challenge/src/setup.sh

RUN cp /flag.txt /home/challenge/src/chroot

ENV TERM=xterm
ENV OPENAI_API_KEY='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'
ENV OPENAI_MODEL='gpt-4-1106-preview'

# The port this leaves on
EXPOSE 11302
CMD ["socat", "TCP-LISTEN:11302,reuseaddr,fork", "EXEC:'/home/challenge/src/service.sh',pty,raw,echo=0,stderr"] # ,su=challenge

# docker rm -f $(docker ps -a -q --filter ancestor=ci_ninja2_high); docker build -t ci_ninja2_high . && docker run -d -p 11302:11302 ci_ninja2_high
# nc localhost 11302