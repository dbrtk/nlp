# this should be ran using python:3.7
FROM python:3.7

RUN groupadd -r nlpuser && useradd -r -g nlpuser nlpuser

RUN mkdir -p /data
# COPY nltk_data /opt/nltk_data

RUN chown -R nlpuser:nlpuser /data


# Copy the current directory contents into the container at /app
COPY . /app

RUN chown -R nlpuser:nlpuser /app

# Set the working directory to /app
WORKDIR /app

# setting up the environment variables for the rmxbot configuration file
ENV DATA_ROOT '/data'

ENV NLTK_DATA_PATH '/opt/nltk_data'

ENV REDIS_HOST_NAME 'redis'

# Install any needed packages specified in requirements.txt
RUN pip install -U pip && pip install -e .


USER nlpuser
