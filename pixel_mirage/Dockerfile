# Start from a PyTorch base image
FROM pytorch/pytorch:latest

# Set the working directory in the Docker container
WORKDIR /src

# Install socat
RUN apt-get update && apt-get install -y socat strace

RUN useradd -u 31337 -ms /bin/bash challenge

# Copy the Python script and additional modules into the container
COPY ./src /src

# Install any additional dependencies
# RUN pip install <your-dependencies-here>

# Ensure the data and submitted directories exist
RUN mkdir -p ./data

EXPOSE 65432

RUN chmod +x /src/server.sh

# CMD ["python", "src/challenge.py"]
# The command to run your script
CMD [ "socat", "TCP-LISTEN:65432,reuseaddr,fork", "EXEC:'/src/server.sh',pty,raw,echo=0"]
