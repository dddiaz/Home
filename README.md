# Home of my personal website

#### @ http://www.dddiaz.com

This is my personal website. It is build with Python, Flask, MongoDB, DynamoDB, and Docker.
It is deployed on AWS using code pipeline to automatically build and deploy changes pushed to Github.  
It also runs my personal blood glucose API that returns real time blood glucose data.

I hope you enjoy checking out the source.  
Nothing is ever perfect, but I am proud of what I have accomplished here.  
If you notice anything out of place, feel free to let me know!

#### Goals:
- Utilize Docker
- Continuous Delivery / Continuous Integration
- Python with Flask
- Blog

#### How to run locally:
- Have docker installed
- Command to build image: docker-compose build
- Command to run the app: docker-compose up

#### Pycharm Run Configuration:
- Really important gotcha! -> if app isnt in debug mode it wont auto reload on code changes (Set this with an env var)
- Make sure you add a debug.config with secrets when running locally in debug mode
```
[Nightscout]
NIGHTSCOUT_DB_CONNECTION_STRING = mongodb:Your-Mongo
NIGHTSCOUT_DB_NAME: Your-Nightscout

[AWS]
AWS_ACCESS_KEY_ID = Your-ID
AWS_SECRET_ACCESS_KEY: Your-Key

```

- Need to set up project interpreter
- Then just update run configuration (which should be committed, but if not...)
- Link: https://blog.jetbrains.com/pycharm/2017/03/docker-compose-getting-flask-up-and-running/


#### Notes for running on aws:
- Need to set up elastic beanstalk with certain env vars
- - Refrence EnvironmentSetupNotes.txt
- - FLASK_IN_DEBUG_MODE
- - NIGHTSCOUT_DB_CONNECTION_STRING
- - NIGHTSCOUT_DB_NAME

#### TODO:
- Travis
- Unit Tests

