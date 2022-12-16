from code_etl.arm import (
    ArmToken,
)
from os import (
    environ,
)


def get_token() -> ArmToken:
    return ArmToken.new(environ["TEST_ARM_TOKEN"])


def get_group() -> str:
    return environ["TEST_ARM_GROUP"]
