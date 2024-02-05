# Use a base Linux image
FROM ubuntu:20.04
FROM python:3.8

WORKDIR /app

# Copy/Create everything needed
COPY server.py /app/server.py
COPY auto.py /app/auto.py
COPY requirements.txt /tmp/requirements.txt
COPY TokSlow.crx /app/TokSlow.crx
RUN mkdir -p /app/stats_data

# Executables
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
COPY chromedriver /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Install Google Chrome
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -r /tmp/requirements.txt

# Set Port and Run Script
EXPOSE 34543 
CMD ["./start.sh"]

# Google chrome fun
# Chrome driver fun + make it executable (downloads chromedriver 114)
# RUN apt-get install -yqq unzip \
#     && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
#     && unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/ \
#     && rm /tmp/chromedriver.zip