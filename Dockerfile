FROM python:3.8

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -U pip && pip install -e .

# creating a directory that will contain nltk_data
RUN mkdir /data

# Download resources for nltk
RUN python -m nltk.downloader -d /data/nltk_data stopwords wordnet averaged_perceptron_tagger punkt

ENV NLTK_DATA_PATH '/data/nltk_data'

ENV REDIS_HOST_NAME 'redis'

# Endpoint of the service that does NMF
ENV NMF_ENDPOINT 'http://rmxnmf:8007'


