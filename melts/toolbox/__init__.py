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
    sorts,
    drills,
)

# Imported but unused
assert api
assert utils
assert constants
assert logger
assert reports
assert toolbox
assert sorts
assert drills

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
