from lib_path.common import (
    get_vulnerabilities_from_iterator_blocking,
)
from model.core_model import (
    FindingEnum,
    Vulnerabilities,
)
from parse_java_properties import (
    load as load_java_properties,
)
from typing import (
    Iterator,
    Tuple,
)


def java_properties_sensitive_data(content: str, path: str) -> Vulnerabilities:
    sensible_key_smells = {
        "amazon.aws.key",
        "amazon.aws.secret",
        "artifactory_user",
        "artifactory_password",
        "aws.accesskey",
        "aws.secretkey",
        "bg.ws.aws.password",
        "bg.ws.key-store-password",
        "bg.ws.trust-store-password",
        "certificate.password",
        "crypto.password",
        "db.password",
        "database.password",
        "facephi.password",
        "jasypt.encryptor.password",
        "jwt.token.basic.signing.secret",
        "key.alias.password",
        "lambda.credentials2.key",
        "lambda.credentials2.secret",
        "mbda.credentials2.secret",
        "micro.password",
        "org.apache.ws.security.crypto.merlin.alias.password",
        "org.apache.ws.security.crypto.merlin.keystore.password",
        "passwordkeystore",
        "sonar.password",
        "spring.datasource.password",
        "spring.mail.password",
        "spring.mail.username",
        "transv-amq-lido4d-user",
        "transv-amq-lido4d-passwd",
        "truststore.password",
        "user_producer_amq",
        "pass_producer_amq",
        "wk-db-fup-lido4d-user",
        "wk-db-fup-lido4d-password",
        "wk-db-lido4d-wabi-user",
        "wk-db-lido4d-wabi-password",
        "wk-db-opshis-lido4d-password",
        "wk-sftp-cms-password",
        "wk-sftp-cms-username",
        "wk-sftp-fup-user",
        "wk-sftp-fup-password",
        "ws.aws.password",
    }

    def iterator() -> Iterator[Tuple[int, int]]:
        data = load_java_properties(
            content,
            include_comments=True,
            exclude_protected_values=True,
        )
        for line_no, (key, val) in data.items():
            key = key.lower()
            for sensible_key_smell in sensible_key_smells:
                if sensible_key_smell in key and val:
                    yield line_no, 0

    return get_vulnerabilities_from_iterator_blocking(
        content=content,
        cwe={"798"},
        description_key="src.lib_path.f009.java_properties_sensitive_data",
        finding=FindingEnum.F009,
        iterator=iterator(),
        path=path,
    )
