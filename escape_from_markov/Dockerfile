FROM python:3.11.6-slim-bookworm

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y socat python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir "/opt/challenge/"
COPY ./src/* "/opt/challenge/"
# RUN pip install -r "/opt/challenge/requirements.txt"
WORKDIR "/opt/challenge/"
RUN chmod +x serve.sh chall.py

EXPOSE 25933
CMD ./serve.sh
