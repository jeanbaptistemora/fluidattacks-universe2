from fluidasserts.helper import (
    crypto,
)
from os import (
    environ,
)

# Encrypt secrets as an encrypted YAML file
crypto.create_encrypted_yaml(
    key_b64=environ["yaml_key_b64"],
    secrets={"user": "Donald Knuth", "password": "asserts"},
)
