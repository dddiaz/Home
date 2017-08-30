"""
This file is too manually insert blog posts into DYNAMO DB
pycharm doesnt seem to connect to the console correctly on the container
in the mean time

sudo docker exec -i -t home_web_1 /bin/bash
python insert_blog_post.py
"""
import uuid
import datetime
import configparser
import boto3


TITLE = "AWS Code Pipeline!"
DESC = "Docker + AWS CodeBuild + AWS Elastic Beanstalk"
# HTML can be injected here
POST = "<p>Coming Soon!</p>" \
       "<p>Yes, he’s lost his left hand, so he’s going to be “all right.” -Doctor</p>"


config_parser = configparser.ConfigParser()
config_parser.read('debug.config')
DYNAMODB = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id=config_parser['AWS']['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=config_parser['AWS']['AWS_SECRET_ACCESS_KEY']
)
blog_table = DYNAMODB.Table('Home-Blog')


if __name__ == '__main__':
    # run the app
    response = blog_table.put_item(Item={
        'UUID': str(uuid.uuid4()),
        'year': 2017,
        'title': TITLE,
        'tags': {
            'test':'test',
        },
        'desc':DESC,
        'post':POST,
        'date': str(datetime.datetime.utcnow()),
        'last_modified': str(datetime.datetime.utcnow())
    })
    print(response)