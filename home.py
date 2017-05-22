import configparser
import os

import boto3
from botocore.exceptions import ClientError
from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# configs
app.config['FLASK_IN_DEBUG_MODE'] = os.getenv('FLASK_IN_DEBUG_MODE', 'False') == 'True'

# Note: Only use this to use pycharm debugger.
# Not sure yet how to inject env var of debug mode into debug container yet
# app.config['FLASK_IN_DEBUG_MODE'] = True

DYNAMODB = None
MONGO_CLIENT =None

if app.config['FLASK_IN_DEBUG_MODE']:
    print("App in DUBUG MODE")
    # use configs from config file in app dir
    config_parser = configparser.ConfigParser()
    config_parser.read('debug.config')
    app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] = config_parser['Nightscout']['NIGHTSCOUT_DB_CONNECTION_STRING']
    app.config['NIGHTSCOUT_DB_NAME'] = config_parser['Nightscout']['NIGHTSCOUT_DB_NAME']
    # set up boto client
    DYNAMODB = boto3.resource(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id=config_parser['AWS']['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=config_parser['AWS']['AWS_SECRET_ACCESS_KEY']
    )
else:
    # use configs in environment specified in the Elastic Beanstalk Console
    app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] = os.getenv('NIGHTSCOUT_DB_CONNECTION_STRING', '')
    app.config['NIGHTSCOUT_DB_NAME'] = os.getenv('NIGHTSCOUT_DB_NAME', '')
    DYNAMODB = boto3.resource('dynamodb', region_name='us-east-1')


# Nightscout db logic
if app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] != '' and app.config['NIGHTSCOUT_DB_NAME'] != '':
    MONGO_CLIENT = MongoClient(app.config['NIGHTSCOUT_DB_CONNECTION_STRING'])
    db = MONGO_CLIENT[app.config['NIGHTSCOUT_DB_NAME']]
    collection = db['entries']

# Dynamo DB Setup
blog_table = DYNAMODB.Table('Home-Blog')


# # Put an item in the db
# response = blog_table.put_item(
#     Item={
#         'UUID': str(uuid.uuid4()),
#         'year': 2017,
#         'title': "Test Blog Title",
#         'tags': {
#             'test':'test',
#         },
#         'desc':"test blog post",
#         'post':"This is the content of a test blog post",
#         'date': str(datetime.datetime.utcnow()),
#         'last_modified': str(datetime.datetime.utcnow())
#         }
# )
# print("PutItem succeeded:")
# print(response)


@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/test-error')
# def test_error():
#     # Just using this to quickly test that prod isn't in debug mode
#     raise OSError


@app.route('/health')
def health():
    return jsonify()

@app.route('/test-blog-post-layout')
def test_blog_post_layout():
    # dummy post
    post = {
        'title': 'Test-Blog-Title',
        'body': 'Beautiful day in SOCAL!'
    }
    return render_template("blog_post.html", post=post)


@app.route('/last-blood-glucose')
def last_blood_glucose():
    if MONGO_CLIENT is None:
        # return nothing because no db connection
        return jsonify()
    # ordering of sort matters and dicts in python are unordered so dont use dict for sort
    res = collection.find_one(sort=[("_id", -1)])
    # handle errors!
    return jsonify(sgv=res['sgv'],
                   date=res['date'],
                   dateString=res['dateString'],
                   trend=res['trend'],
                   direction=res['direction'])


@app.route('/blog')
def show_entries():
    return render_template("blog.html")


@app.route('/blog/<post_id>')
def show_entry(post_id):
    """
    Will return the specified post
    #c6d68d74-de2b-4406-b5c7-879a6b7d5bd7
    Look here for refrence:
    http://docs.aws.amazon.com/amazondynamodb/latest/gettingstartedguide/GettingStarted.Python.03.html
    :param post_id: 
    :return: 
    """
    try:
        response = blog_table.get_item(
            Key={'UUID': post_id}
        )
    except ClientError as e:
        #print(e.response['Error']['Message'])
        pass
    else:
        item = response['Item']
        return render_template("blog_post.html", post=item)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Need to set host to access outside of container
    app.run(debug=app.config['FLASK_IN_DEBUG_MODE'], host='0.0.0.0')
