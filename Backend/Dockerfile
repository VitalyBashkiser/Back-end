# Use the Python image
FROM python:3.10.13

# Set up a working directory inside the container
WORKDIR /Backend

# Install net-tools for networking utilities
RUN apt-get update && apt-get install -y net-tools

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt inside the container
COPY ../requirements.txt .

# Upgrade pip & install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the .env file inside the container
COPY .env .

# Copy all other project files
COPY . .

# Copy start.sh inside the container
COPY start.sh .

# Give permissions to run the script
RUN chmod +x start.sh

# Expose the port your app runs on
EXPOSE 8000

# The command to run Django
CMD ["sh", "start.sh"]