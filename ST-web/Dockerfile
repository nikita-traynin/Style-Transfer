FROM python:3.9

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "autoapp", "run", "--host", "0.0.0.0"]