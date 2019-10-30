"""Test methods of fluidasserts.cloud.cloudformation.rds module."""

# local imports
from fluidasserts.cloud.aws.cloudformation import rds


# Constants
RDS_SAFE: str = 'test/static/cloudformation/rds-safe/template.yml'
RDS_VULNERABLE: str = 'test/static/cloudformation/rds-vulnerable/template.yml'
NOT_EXISTS_PATH: str = 'test/static/cloudformation/not-exists/template.yml'


def test_has_unencrypted_storage():
    """test rds.has_unencrypted_storage."""
    assert rds.has_unencrypted_storage(RDS_VULNERABLE).is_open()
    assert rds.has_unencrypted_storage(RDS_SAFE).is_closed()
    assert rds.has_unencrypted_storage(NOT_EXISTS_PATH).is_unknown()
