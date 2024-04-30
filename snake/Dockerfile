FROM ubuntu:20.04

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y  python3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -u 31337 -ms /bin/bash challenge
RUN chown root:root /home/challenge

# Source files
COPY snake /home/challenge/snake
WORKDIR /home/challenge/snake

RUN chmod 755 -R /home/challenge/

# The port this leaves on
EXPOSE 8080
CMD ["python3", "-m", "http.server", "8080"]