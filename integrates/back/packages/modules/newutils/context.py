# Standard
import os


API_STATUS = os.environ['API_STATUS']
AWS_DYNAMODB_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
AWS_DYNAMODB_SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_SESSION_TOKEN = os.environ.get('AWS_SESSION_TOKEN')
DB_MODEL_PATH = os.environ['INTEGRATES_DB_MODEL_PATH']
CHARTS_LOGO_PATH = os.environ['INTEGRATES_CHARTS_LOGO_PATH']
CI_COMMIT_REF_NAME = os.environ['CI_COMMIT_REF_NAME']
DYNAMODB_HOST = os.environ['DYNAMODB_HOST']
DYNAMODB_PORT = os.environ['DYNAMODB_PORT']
ENVIRONMENT = os.environ['ENVIRONMENT']
