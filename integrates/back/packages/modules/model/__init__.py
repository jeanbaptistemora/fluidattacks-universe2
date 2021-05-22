import json

from dynamodb.context import DB_MODEL_PATH
from dynamodb.table import load_table


with open(DB_MODEL_PATH, mode="r") as file:
    TABLE = load_table(json.load(file))
