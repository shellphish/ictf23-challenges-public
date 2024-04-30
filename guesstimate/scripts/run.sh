#!/bin/bash
IMAGE_NAME=guesstimate
PORT=15151
docker run -m 16g -p ${PORT}:${PORT} ${IMAGE_NAME}
