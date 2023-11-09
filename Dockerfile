# Use a base Linux image
FROM ubuntu:20.04
FROM python:3.8
# Install necessary packages and dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip
# Copy your extension and Python script to the image
COPY /chrome_extension /app/chrome-extension
COPY server.py /app/python-script.py
COPY /stats_data /app/stats_data
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt
# Set the working directory
WORKDIR /app
# Command to run your Python script
EXPOSE 34543
CMD ["python3", "python-script.py"]
