# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from lib_root.f052.c_sharp import (
    c_sharp_disabled_strong_crypto,
    c_sharp_insecure_cipher,
    c_sharp_insecure_hash,
    c_sharp_insecure_keys,
    c_sharp_insecure_rijndael_managed,
    c_sharp_managed_secure_mode,
    c_sharp_obsolete_key_derivation,
    c_sharp_rsa_secure_mode,
)
from lib_root.f052.go import (
    go_insecure_cipher,
    go_insecure_hash,
)
from lib_root.f052.java import (
    java_insecure_cipher,
    java_insecure_cipher_jmqi,
    java_insecure_cipher_ssl,
    java_insecure_connection,
    java_insecure_hash,
    java_insecure_hash_argument,
    java_insecure_key_ec,
    java_insecure_key_rsa,
    java_insecure_key_secret,
    java_insecure_pass,
)
from lib_root.f052.javascript import (
    javascript_insecure_create_cipher,
    javascript_insecure_ec_keypair,
    javascript_insecure_ecdh_key,
    javascript_insecure_encrypt,
    javascript_insecure_hash,
    javascript_insecure_rsa_keypair,
)
from lib_root.f052.kotlin import (
    kotlin_insecure_cipher,
    kotlin_insecure_hash,
    kotlin_insecure_key,
)
from lib_root.f052.typescript import (
    ts_insecure_aes_cipher,
    ts_insecure_ciphers,
    ts_insecure_create_cipher,
)
from model import (
    core_model,
    graph_model,
)

FINDING: core_model.FindingEnum = core_model.FindingEnum.F052
QUERIES: graph_model.Queries = (
    (FINDING, c_sharp_insecure_hash),
    (FINDING, c_sharp_insecure_cipher),
    (FINDING, c_sharp_managed_secure_mode),
    (FINDING, c_sharp_insecure_rijndael_managed),
    (FINDING, c_sharp_rsa_secure_mode),
    (FINDING, c_sharp_insecure_keys),
    (FINDING, c_sharp_disabled_strong_crypto),
    (FINDING, c_sharp_obsolete_key_derivation),
    (FINDING, go_insecure_cipher),
    (FINDING, go_insecure_hash),
    (FINDING, java_insecure_cipher),
    (FINDING, java_insecure_cipher_ssl),
    (FINDING, java_insecure_cipher_jmqi),
    (FINDING, java_insecure_connection),
    (FINDING, java_insecure_hash),
    (FINDING, java_insecure_hash_argument),
    (FINDING, java_insecure_key_ec),
    (FINDING, java_insecure_key_rsa),
    (FINDING, java_insecure_key_secret),
    (FINDING, java_insecure_pass),
    (FINDING, javascript_insecure_create_cipher),
    (FINDING, javascript_insecure_encrypt),
    (FINDING, javascript_insecure_hash),
    (FINDING, javascript_insecure_ecdh_key),
    (FINDING, javascript_insecure_ec_keypair),
    (FINDING, javascript_insecure_rsa_keypair),
    (FINDING, kotlin_insecure_cipher),
    (FINDING, kotlin_insecure_hash),
    (FINDING, kotlin_insecure_key),
    (FINDING, ts_insecure_aes_cipher),
    (FINDING, ts_insecure_ciphers),
    (FINDING, ts_insecure_create_cipher),
)
