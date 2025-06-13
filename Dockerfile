# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "todo-app.py"]

