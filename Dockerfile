FROM python:3.9

# Install required libraries
RUN pip install requests watchdog

# Set the working directory
WORKDIR /app

# Copy the Python script to the container
COPY ts_ssh_notify.py /app/ts_ssh_notify.py

# Expose the volume mount point
VOLUME /data

# Set the command to execute on start
CMD ["python", "ts_ssh_notify.py"]
