import configparser
import os
from botocore.exceptions import ClientError
from flask import Flask, render_template, jsonify
from persistance import blog, glucose

app = Flask(__name__)

# Configs
app.config['FLASK_IN_DEBUG_MODE'] = os.getenv('FLASK_IN_DEBUG_MODE', 'False') == 'True'
if app.config['FLASK_IN_DEBUG_MODE']:
    # use configs from config file in app dir
    config_parser = configparser.ConfigParser()
    config_parser.read('debug.config')
    app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] = config_parser['Nightscout']['NIGHTSCOUT_DB_CONNECTION_STRING']
    app.config['NIGHTSCOUT_DB_NAME'] = config_parser['Nightscout']['NIGHTSCOUT_DB_NAME']
    app.config['AWS_ACCESS_KEY_ID'] = config_parser['AWS']['AWS_ACCESS_KEY_ID']
    app.config['AWS_SECRET_ACCESS_KEY'] = config_parser['AWS']['AWS_SECRET_ACCESS_KEY']
else:
    # use configs in environment specified in the Elastic Beanstalk Console
    app.config['NIGHTSCOUT_DB_CONNECTION_STRING'] = os.getenv('NIGHTSCOUT_DB_CONNECTION_STRING', '')
    app.config['NIGHTSCOUT_DB_NAME'] = os.getenv('NIGHTSCOUT_DB_NAME', '')
    # AWS will already be set up on elastic beanstalk

GlucoseValues = glucose.GlucoseValuesDB(app)
BlogPosts = blog.BlogPostsDB(app)

@app.route('/')
def index():
    return render_template("index.html")


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
    return GlucoseValues.last_glucose_value()


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
    # TODO : abstract this out
    try:
        response = BlogPosts.blog_table.get_item(
            Key={'UUID': post_id}
        )
    except ClientError as e:
        pass
    else:
        # If searched item doesnt exist, redirect to index
        # in future redirect to blog home
        if 'Item' not in response.keys():
            return render_template('index.html')
        item = response['Item']
        return render_template("blog_post.html", post=item)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # Need to set host to access outside of container
    app.run(debug=app.config['FLASK_IN_DEBUG_MODE'], host='0.0.0.0')
