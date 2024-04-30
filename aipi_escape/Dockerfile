FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y coreutils build-essential socat python3 python3-pip \
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
RUN chmod 700 /home/challenge/src/setup.sh
RUN chmod 755 /home/challenge/src/service.sh
RUN chmod 755 /home/challenge/src/rate_limiting_client.py
RUN chmod 755 /home/challenge/src/aipi_escape.py

# Install the service
WORKDIR /home/challenge/src
RUN /home/challenge/src/setup.sh

ENV TERM=xterm
ENV OPENAI_API_KEY='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'
ENV OPENAI_MODEL='gpt-3.5-turbo'

# The port this leaves on
EXPOSE 11303
CMD ["socat", "TCP-LISTEN:11303,reuseaddr,fork", "EXEC:'/home/challenge/src/service.sh',pty,raw,echo=0,stderr,su=challenge"]

# docker rm -f $(docker ps -a -q --filter ancestor=aipi_escape); docker build -t aipi_escape . && docker run -d -p 11303:11303 aipi_escape
# nc localhost 11303
