import os

SCHEMAS_DIR: str = "____schemas"
RECORDS_DIR: str = "____records"
STATE_DIR: str = "____state"


def prepare_env() -> None:
    """Create/reset the staging area."""
    for _dir in (RECORDS_DIR, SCHEMAS_DIR, STATE_DIR):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        else:
            for file in os.listdir(_dir):
                os.remove(f"{_dir}/{file}")


def release_env() -> None:
    """Clean the staging area on exit."""
    for _dir in (SCHEMAS_DIR, RECORDS_DIR, STATE_DIR):
        for file in os.listdir(_dir):
            os.remove(f"{_dir}/{file}")
        os.removedirs(f"{_dir}")
