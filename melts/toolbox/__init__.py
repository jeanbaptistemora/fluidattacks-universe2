# Standard library
import sys

# Local imports
from toolbox import (
    api,
    utils,
    constants,
    logger,
    reports,
    toolbox,
    drills,
)

# Imported but unused
assert api
assert utils
assert constants
assert logger
assert reports
assert toolbox
assert drills

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
