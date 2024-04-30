FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y xinetd  python3 python3-pip netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install openai=="0.28.1" gmpy2 fire

COPY ./writeup/flag.txt /flag

RUN chmod 444 /flag

RUN useradd -u 31337 -ms /bin/bash challenge
RUN chown root:root /home/challenge

# Source files
COPY src /home/challenge/src
WORKDIR /home/challenge

RUN chmod 755 -R /home/challenge/
RUN mv /home/challenge/src/xinetd.conf /etc/xinetd.d/aicalc

ENV API_KEY='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'

# The port this leaves on
EXPOSE 11239
CMD ["/usr/sbin/xinetd", "-dontfork"]