from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)

@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == '__main__':
    # This is here so we can access the web app from outside the container
    app.run(debug=True, host='0.0.0.0')
