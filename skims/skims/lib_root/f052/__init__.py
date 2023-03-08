from lib_root.f052.c_sharp import (
    c_sharp_disabled_strong_crypto,
    c_sharp_insecure_cipher,
    c_sharp_insecure_hash,
    c_sharp_insecure_keys,
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
    javascript_insec_msg_auth_mechanism,
    javascript_insecure_create_cipher,
    javascript_insecure_ec_keypair,
    javascript_insecure_ecdh_key,
    javascript_insecure_encrypt,
    javascript_insecure_hash,
    javascript_insecure_hash_library,
    javascript_insecure_rsa_keypair,
    javascript_jwt_insec_sign_algo_async,
    javascript_jwt_insec_sign_algorithm,
)
from lib_root.f052.kotlin import (
    kotlin_insecure_certification,
    kotlin_insecure_cipher,
    kotlin_insecure_cipher_http,
    kotlin_insecure_cipher_ssl,
    kotlin_insecure_hash,
    kotlin_insecure_hash_instance,
    kotlin_insecure_hostname_ver,
    kotlin_insecure_init_vector,
    kotlin_insecure_key_ec,
    kotlin_insecure_key_rsa,
)
from lib_root.f052.python import (
    python_insecure_cipher,
)
from lib_root.f052.swift import (
    swift_insecure_cipher,
    swift_insecure_cryptalgo,
    swift_insecure_crypto,
)
from lib_root.f052.typescript import (
    typescript_insec_msg_auth_mechanism,
    typescript_insecure_create_cipher,
    typescript_insecure_ec_keypair,
    typescript_insecure_ecdh_key,
    typescript_insecure_encrypt,
    typescript_insecure_hash,
    typescript_insecure_hash_library,
    typescript_insecure_rsa_keypair,
    typescript_jwt_insec_sign_algo_async,
    typescript_jwt_insec_sign_algorithm,
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
    (FINDING, javascript_insecure_hash_library),
    (FINDING, javascript_insecure_ecdh_key),
    (FINDING, javascript_insecure_ec_keypair),
    (FINDING, javascript_insecure_rsa_keypair),
    (FINDING, javascript_jwt_insec_sign_algo_async),
    (FINDING, javascript_insec_msg_auth_mechanism),
    (FINDING, javascript_jwt_insec_sign_algorithm),
    (FINDING, kotlin_insecure_cipher),
    (FINDING, kotlin_insecure_cipher_http),
    (FINDING, kotlin_insecure_cipher_ssl),
    (FINDING, kotlin_insecure_hash),
    (FINDING, kotlin_insecure_hash_instance),
    (FINDING, kotlin_insecure_key_ec),
    (FINDING, kotlin_insecure_key_rsa),
    (FINDING, kotlin_insecure_init_vector),
    (FINDING, kotlin_insecure_hostname_ver),
    (FINDING, kotlin_insecure_certification),
    (FINDING, python_insecure_cipher),
    (FINDING, swift_insecure_cipher),
    (FINDING, swift_insecure_crypto),
    (FINDING, swift_insecure_cryptalgo),
    (FINDING, typescript_insecure_create_cipher),
    (FINDING, typescript_insecure_hash),
    (FINDING, typescript_insecure_hash_library),
    (FINDING, typescript_insecure_encrypt),
    (FINDING, typescript_insecure_ecdh_key),
    (FINDING, typescript_insecure_ec_keypair),
    (FINDING, typescript_insecure_rsa_keypair),
    (FINDING, typescript_jwt_insec_sign_algorithm),
    (FINDING, typescript_insec_msg_auth_mechanism),
    (FINDING, typescript_jwt_insec_sign_algo_async),
)
