import json

from context import FI_DB_MODEL_PATH
from dynamodb.table import load_table


with open(FI_DB_MODEL_PATH, mode="r") as file:
    TABLE = load_table(json.load(file))
