#!/bin/bash

# Check if a container ID/name was passed as an argument
if [ $# -eq 0 ]
then
    echo "Usage: $0 <container-id-or-name>"
    exit 1
fi

container_id=$1

# Check if the container is running
if ! docker ps --format '{{.Names}}' | grep -w "$container_id" &> /dev/null
then
    echo "Container with ID/name '$container_id' is not running."
    exit 1
fi

# Start an interactive shell session inside the container
echo "Starting an interactive shell inside the container '$container_id'..."
docker exec -it "$container_id" /bin/bash
