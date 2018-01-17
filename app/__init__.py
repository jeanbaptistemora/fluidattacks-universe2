import os

try:
    AWS_ACCESS_KEY_DYNAMODB = os.environ['AWS_ACCESS_KEY_DYNAMODB']
    AWS_SECRET_KEY_DYNAMODB = os.environ['AWS_SECRET_KEY_DYNAMODB']
    AWS_REGION = os.environ['AWS_REGION']
except KeyError as e:
    print "Environment variable " + e.args[0] +  " doesn't exist" 
    raise
