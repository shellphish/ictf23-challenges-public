FROM gcc

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y xinetd \
    && apt-get install --no-install-recommends -y socat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -u 31337 -ms /bin/bash challenge
# Prevents the user from writing to the home directory
RUN chown root:root /home/challenge
RUN chmod 755 /home/challenge

# Source files
COPY src /home/challenge/src
# Writeable files
COPY rw /home/challenge/rw
RUN chown challenge:challenge /home/challenge/rw
RUN chmod 755 /home/challenge/rw
RUN chmod +x /home/challenge/src/rps.py


# Creates the application
WORKDIR /home/challenge/src
# Install the service
RUN mv /home/challenge/src/xinetd.conf /etc/xinetd.d/rps

# The port this leaves on
EXPOSE 7283
# CMD ["/usr/sbin/xinetd", "-dontfork"]
CMD socat TCP-LISTEN:7283,reuseaddr,fork EXEC:"./rps.py"
