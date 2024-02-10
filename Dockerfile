# Use a base Linux image
FROM ubuntu:20.04
FROM python:3.8

WORKDIR /app

# Copy/Create everything needed
COPY tokgrab.py /app/tokgrab.py
COPY requirements.txt /tmp/requirements.txt
COPY /browser_scripts /app/
COPY /chromefiles /app/

RUN mkdir -p /app/stats_data
RUN mkdir -p /app/pcaplogs

# Install dependencies and Google Chrome
RUN apt-get update \
    && apt-get install -y /app/chromefiles/google-chrome-stable_current_amd64.deb \
    && rm /app/google-chrome-stable_current_amd64.deb
RUN python3 -m pip install -r /tmp/requirements.txt

