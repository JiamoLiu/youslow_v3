# Use a base Linux image
FROM ubuntu:20.04
FROM python:3.8

# Copy/Create everything needed
COPY /TokSlow /app/TokSlow
COPY server.py /app/server.py
COPY auto.py /app/auto.py
COPY requirements.txt /tmp/requirements.txt
RUN mkdir -p /app/stats_data

# Executables
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
COPY chromedriver /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# Run all updates and dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
RUN apt-get update && apt-get install -y wget gnupg \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm ./google-chrome-stable_current_amd64.deb
RUN python3 -m pip install -r /tmp/requirements.txt

# Set the working directory
WORKDIR /app

# Set Port and Run Script
EXPOSE 34543 
CMD ["./start.sh"]

# Google chrome fun
# Chrome driver fun + make it executable (downloads chromedriver 114)
# RUN apt-get install -yqq unzip \
#     && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip \
#     && unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/ \
#     && rm /tmp/chromedriver.zip