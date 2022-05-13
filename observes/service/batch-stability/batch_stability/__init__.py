import bugsnag
from os import (
    environ,
)

# Constants
__version__ = "2.0.0"
NOTIFIER_KEY = environ.get("bugsnag_notifier_key", "")

# Side effects
bugsnag.configure(  # type: ignore[no-untyped-call]
    api_key=NOTIFIER_KEY,
    asynchronous=False,
    send_code=False,
)
