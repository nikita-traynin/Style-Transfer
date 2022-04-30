FROM ubuntu

WORKDIR /project

COPY requirements.txt requirements.txt

RUN apt update && \
    apt-get install -y python3.10 && \
    apt-get install -y python3.10-venv && \
    python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install -r requirements.txt

COPY dockertest.py dockertest.py

CMD ["python3", "-m",  "dockertest"]
