# Use an official Python rutime as a parent image
FROM node:carbon

# Set the working directory to /app
WORKDIR /app

# Copy the current direcotry contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt

EXPOSE 80

# Define Environment Variable
ENV NAME World


