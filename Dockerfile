# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Install git
RUN apt-get update && apt-get install -y git

# Clone the repository
RUN git clone --branch test1 https://github.com/Proteus1963/ramadrama.git .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 5555

CMD ["python", "ramascrape.py"]
