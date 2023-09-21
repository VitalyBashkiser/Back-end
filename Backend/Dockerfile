# Dockerfile

# Use the Python image
FROM python:3.10.13

# Set up a working directory inside the container
WORKDIR /Backend

# Copy requirements.txt inside the container
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy all other project files
COPY . .

COPY . start.sh

# Give permissions to run the script
RUN chmod +x start.sh

# The command to run Django
CMD ["sh", "./start.sh"]
