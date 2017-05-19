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
    debug_mode = os.getenv('FLASK_IN_DEBUG_MODE', 'False') == 'True'
    # Need to set host to access outside of container
    app.run(debug=debug_mode, host='0.0.0.0')
