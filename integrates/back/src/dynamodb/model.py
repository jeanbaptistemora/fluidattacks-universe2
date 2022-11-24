from context import (
    FI_DB_MODEL_PATH,
)
from dynamodb import (
    tables,
)
import json

with open(FI_DB_MODEL_PATH, mode="r", encoding="utf-8") as file:
    TABLE = tables.load_tables(json.load(file))[0]
