from datetime import (
    datetime,
)

COMMIT_HASH_SENTINEL: str = "-" * 40
DATE_SENTINEL: datetime = datetime.utcfromtimestamp(0)
DATE_NOW: datetime = datetime.utcnow()
