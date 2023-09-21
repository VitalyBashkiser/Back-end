# Dockerfile

# Use the Python image
FROM python:3.10.13

# Set up a working directory inside the container
WORKDIR /Backend

# Copy requirements.txt inside the container
COPY python/Back-end/Backend/requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy all other project files
COPY python/Back-end/Backend .

# The command to run Django
CMD ["python", "manage.py", "runserver", "0.0.0.0.0:8000"]
