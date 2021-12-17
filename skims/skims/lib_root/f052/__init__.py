from lib_root.f052.c_sharp import (
    c_sharp_aesmanaged_secure_mode,
    c_sharp_insecure_cipher,
    c_sharp_insecure_hash,
    c_sharp_insecure_keys,
    c_sharp_rsa_secure_mode,
)
from lib_root.f052.go import (
    go_insecure_cipher,
    go_insecure_hash,
)
from lib_root.f052.java import (
    java_insecure_cipher,
    java_insecure_hash,
    java_insecure_key,
    java_insecure_pass,
)
from lib_root.f052.javascript import (
    javascript_insecure_cipher,
    javascript_insecure_hash,
    javascript_insecure_key,
)
from lib_root.f052.kotlin import (
    kotlin_insecure_cipher,
    kotlin_insecure_hash,
    kotlin_insecure_key,
)
from model import (
    core_model,
    graph_model,
)

# Constants
FINDING: core_model.FindingEnum = core_model.FindingEnum.F052
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_insecure_hash),
    (FINDING, c_sharp_insecure_cipher),
    (FINDING, c_sharp_aesmanaged_secure_mode),
    (FINDING, c_sharp_rsa_secure_mode),
    (FINDING, c_sharp_insecure_keys),
    (FINDING, go_insecure_cipher),
    (FINDING, go_insecure_hash),
    (FINDING, java_insecure_cipher),
    (FINDING, java_insecure_hash),
    (FINDING, java_insecure_key),
    (FINDING, java_insecure_pass),
    (FINDING, javascript_insecure_cipher),
    (FINDING, javascript_insecure_key),
    (FINDING, javascript_insecure_hash),
    (FINDING, kotlin_insecure_cipher),
    (FINDING, kotlin_insecure_hash),
    (FINDING, kotlin_insecure_key),
)
