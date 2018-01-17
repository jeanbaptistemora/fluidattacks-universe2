import os

try:
    AWS_REGION = os.environ['AWS_REGION']
    SECRET_KEY_ENV = os.environ['SECRET_KEY_ENV']
    DB_USER = os.environ['DB_USER']
    DB_PASSWD = os.environ['DB_PASSWD']
    DB_HOST = os.environ['DB_HOST']
    DB_PORT = os.environ['DB_PORT']
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET = os.environ['AWS_SECRET']
    MIXPANEL = os.environ['MIXPANEL']
    INTERCOM = os.environ['INTERCOM']
    INTERCOM_SECURE_KEY_ENV = os.environ['INTERCOM_SECURE_KEY_ENV']
    SLACK_BOT = os.environ['SLACK_BOT']
    GOOGLE_OAUTH2_KEY = os.environ['GOOGLE_OAUTH2_KEY']
    GOOGLE_OAUTH2_SECRET = os.environ['GOOGLE_OAUTH2_SECRET']
    AZUREAD_OAUTH2_KEY = os.environ['AZUREAD_OAUTH2_KEY']
    AZUREAD_OAUTH2_SECRET = os.environ['AZUREAD_OAUTH2_SECRET']
    DRIVE_AUTHORIZATION = os.environ['DRIVE_AUTHORIZATION']
    AWS_OUTPUT = os.environ['AWS_OUTPUT']
except KeyError as e:
    print "Environment variable " + e.args[0] +  " doesn't exist"
    raise
