# Use the official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV DB_USERNAME=your_db_username
ENV DB_PASSWORD=your_db_password
ENV DB_HOST=your_rds_endpoint
ENV DB_NAME=your_db_name

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 4000 available to the world outside this container
EXPOSE 4000

# Run app.py when the container launches
CMD ["python", "app.py"]

