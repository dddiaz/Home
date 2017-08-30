import boto3


class BlogPostsDB:
    def __init__(self, app):
        if app.config['FLASK_IN_DEBUG_MODE']:
            # Check that if in debug mode, the debug config has been set up
            if app.config['AWS_ACCESS_KEY_ID'] == '' or app.config['AWS_SECRET_ACCESS_KEY'] == '':
                print("No AWS Acess Keys. Did you set up the debug.config?")
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name='us-east-1',
                aws_access_key_id= app.config['AWS_ACCESS_KEY_ID'],
                aws_secret_access_key= app.config['AWS_SECRET_ACCESS_KEY'])
        else:
            self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        self.blog_table = self.dynamodb.Table('Home-Blog')