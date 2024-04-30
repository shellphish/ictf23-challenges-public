FROM python:3.9-slim-bookworm

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y socat git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir "/opt/supermart"
COPY ./src/* "/opt/supermart/"
RUN pip install -r "/opt/supermart/requirements.txt"
WORKDIR "/opt/supermart/"
RUN chmod +x serve.sh chall.py

EXPOSE 25931
CMD ./serve.sh
