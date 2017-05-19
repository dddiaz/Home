import os
from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test-error')
def test_error():
    # Just using this to quickly test that prod isn't in debug mode
    raise OSError


if __name__ == '__main__':
    # This is here so we can access the web app from outside the container
    app.run(debug=os.environ['FLASK_IN_DEBUG_MODE'], host='0.0.0.0')
