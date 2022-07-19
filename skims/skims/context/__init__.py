import os

try:
    FI_AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    FI_AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    FI_AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
    FI_DB_MODEL_PATH = os.environ["SKIMS_DB_MODEL_PATH"]
    FI_DYNAMODB_HOST = os.environ["DYNAMODB_HOST"]
    FI_DYNAMODB_PORT = os.environ["DYNAMODB_PORT"]
    FI_ENVIRONMENT = os.environ["ENVIRONMENT"]

    # not secrets but must be environment vars
    FI_AWS_REGION_NAME = "us-east-1"
except KeyError as exe:
    print("Environment variable " + exe.args[0] + " doesn't exist")
    raise
