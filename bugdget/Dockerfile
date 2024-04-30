FROM python:3.11.6-slim-bookworm

RUN apt-get update -y \
    && apt-get install --no-install-recommends -y socat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir "/opt/bugdget"
COPY ./src/* "/opt/bugdget/"
RUN pip install -r "/opt/bugdget/requirements.txt"
WORKDIR "/opt/bugdget/"
RUN chmod +x serve.sh chall.py

EXPOSE 25931
CMD ./serve.sh
