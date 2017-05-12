from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World with Docker!'


if __name__ == '__main__':
    # This is here so we can access the web app from outside the container
    app.run(host='0.0.0.0')
