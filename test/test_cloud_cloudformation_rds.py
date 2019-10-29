"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.cloudformation import rds


# Constants
RDS_SAFE: str = 'test/static/cloudformation/rds-safe/template.yml'
RDS_VULNERABLE: str = 'test/static/cloudformation/rds-vulnerable/template.yml'
NOT_EXISTS_PATH: str = 'test/static/cloudformation/not-exists/template.yml'

#
# Open tests
#


def test_instance_public_open():
    """test rds.has_unencrypted_storage."""
    assert rds.has_unencrypted_storage(RDS_VULNERABLE).is_open()


#
# Closing tests
#


def test_instance_public_close():
    """test rds.has_unencrypted_storage."""
    assert rds.has_unencrypted_storage(RDS_SAFE).is_closed()


#
# Closing tests
#


def test_instance_public_unknown():
    """test rds.has_unencrypted_storage."""
    assert rds.has_unencrypted_storage(NOT_EXISTS_PATH).is_unknown()
