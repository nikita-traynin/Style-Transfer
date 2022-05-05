FROM ubuntu:latest

WORKDIR /project

COPY requirements.txt ./

# Install python, pip, venv, and project dependencies
RUN apt update && \
    apt-get install -y python3-pip && \
    pip install -r requirements.txt

COPY flask_config.toml views.py templates ./
COPY templates templates
COPY static static

CMD ["python3", "-m", "views"]