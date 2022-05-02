FROM ubuntu:latest

WORKDIR /project

COPY requirements.txt requirements.txt

# Install python, pip, venv, and project dependencies
RUN apt update && \
    apt-get install -y python3.10 && \
    apt-get install -y python3-pip && \
    pip3 install -r requirements.txt

COPY dockertest.py dockertest.py

CMD ["python3", "-m", "dockertest"]
