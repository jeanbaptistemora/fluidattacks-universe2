from lib_root.utilities.go import (
    yield_member_access,
    yield_object_creation,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from model.graph_model import (
    GraphDB,
    GraphShardNodes,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def insecure_hash(
    graph_db: GraphDB,
) -> Vulnerabilities:

    insecure_ciphers = {"md4", "md5", "ripemd160", "sha1"}

    def n_ids() -> GraphShardNodes:
        yield from yield_object_creation(graph_db, insecure_ciphers)

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Go"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


def insecure_cipher(
    graph_db: GraphDB,
) -> Vulnerabilities:
    insecure_ciphers = {
        "des",
        "NewTripleDESCipher",
    }

    def n_ids() -> GraphShardNodes:
        yield from yield_member_access(graph_db, insecure_ciphers)
        yield from yield_object_creation(graph_db, insecure_ciphers)

    return get_vulnerabilities_from_n_ids(
        cwe=("310", "327"),
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Go"),
        finding=FINDING,
        graph_shard_nodes=n_ids(),
    )


FINDING: FindingEnum = FindingEnum.F052
