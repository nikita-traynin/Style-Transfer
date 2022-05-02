from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hi stranger'


@app.route('/<name>')
def hello(name):
    return 'Hello world, ' + str(name) + ', from docker!!'


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
