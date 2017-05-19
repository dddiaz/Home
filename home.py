import os
from flask import Flask, render_template

#from boto3 import dynamodb
import boto3

app = Flask(__name__)
app.config.from_object(__name__)

#app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

#somehow check if session is set up or we are in dev so use local env variables
#maybe if app.debug is true or dev environmental variable

# if "AWS_ACCESS_KEY_ID" in os.environ:
#     print("jngfdjksngjsnjfsf")
# else:
#     print("nooooooo")
#
# client = boto3.resource('dynamodb',
#                       region_name='us-east-1',
#                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
#                       aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
# table = client.Table('Home-Blog')
# print(table.creation_date_time)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/test')
def hello_world():
    # fetch specific
    raise OSError


if __name__ == '__main__':
    # This is here so we can access the web app from outside the container
    app.run(debug=True, host='0.0.0.0')
