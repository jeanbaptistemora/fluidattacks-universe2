from lib_ssl.suites import (
    SSLVersionId,
    SSLVersionName,
)
from lib_ssl.types import (
    SSLSettings,
    SSLVulnerability,
)
from model.core_model import (
    LocalesEnum,
)
from typing import (
    Dict,
)
from utils.string import (
    make_snippet,
    SNIPPETS_COLUMNS,
    SnippetViewport,
)


def ssl_name2ssl_id(ssl_name: SSLVersionName) -> int:
    return getattr(SSLVersionId, ssl_name.name).value


def ssl_id2ssl_name(ssl_id: SSLVersionId) -> str:
    return getattr(SSLVersionName, ssl_id.name).value


class SnippetConstructor:
    null = "---"

    # pylint: disable=unused-argument
    def get_target(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Target: " + self.null

    def get_intention(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Intention " + self.null

    def get_versions(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Versions: " + self.null

    def get_request(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Request: " + self.null

    def get_response(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Response: " + self.null

    def get_result(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Result: " + self.null

    def construct(self, ssl_vulnerability: SSLVulnerability) -> str:
        return (
            "{target}\n"
            "{intention}\n"
            "{versions}\n"
            "{request}\n"
            "{response}\n"
            "{result}\n"
        ).format(
            target=self.get_target(ssl_vulnerability),
            intention=self.get_intention(ssl_vulnerability),
            versions=self.get_versions(ssl_vulnerability),
            request=self.get_request(ssl_vulnerability),
            response=self.get_response(ssl_vulnerability),
            result=self.get_result(ssl_vulnerability),
        )


class SnippetConstructorEN(SnippetConstructor):
    # pylint: disable=no-self-use
    def get_target(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Target: {ssl_vulnerability.get_context()}"

    def get_intention(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Intention: {ssl_vulnerability.get_intention(LocalesEnum.EN)}"

    def get_versions(self, ssl_vulnerability: SSLVulnerability) -> str:
        tls_vers = ssl_vulnerability.get_context().get_supported_tls_versions()
        versions = ", ".join([ssl_id2ssl_name(v_id) for v_id in tls_vers])
        return f"TLS versions on server: {versions}"

    def get_request(self, ssl_vulnerability: SSLVulnerability) -> str:
        ssl_settings: SSLSettings = ssl_vulnerability.ssl_settings

        return (
            "Request:\n"
            "    Fallback scsv: {scsv}\n"
            "    TLS version: {tls_version}\n"
            "    Key exchange: {key_exchange}\n"
            "    Authentication: {authentication}\n"
            "    Cipher: {cipher}\n"
            "    Hash: {ssl_hash}"
        ).format(
            scsv=ssl_settings.scsv,
            tls_version=ssl_id2ssl_name(ssl_settings.tls_version),
            key_exchange=", ".join(ssl_settings.key_exchange_names),
            authentication=", ".join(ssl_settings.authentication_names),
            cipher=", ".join(ssl_settings.cipher_names),
            ssl_hash=", ".join(ssl_settings.hash_names),
        )

    def get_response(self, ssl_vulnerability: SSLVulnerability) -> str:
        response = ssl_vulnerability.server_response
        default = "Response:\n    ---"

        if response is None:
            return default

        if response.alert is not None:
            return (
                "Response:\n"
                "    Type: ALERT\n"
                "    Level: {level}\n"
                "    Description: {description}"
            ).format(
                level=response.alert.level.name,
                description=response.alert.description.name,
            )

        if response.handshake is not None:
            return (
                "Response:\n"
                "    Version: {version}\n"
                "    Selected cipher suite:\n"
                "        Iana name: {iana_name}\n"
                "        Openssl name: {openssl_name}\n"
                "        Code: {code}\n"
                "        Vulnerabilities: {vulns}"
            ).format(
                version=ssl_id2ssl_name(response.handshake.version_id),
                iana_name=response.handshake.cipher_suite.iana_name,
                openssl_name=response.handshake.cipher_suite.openssl_name,
                code=response.handshake.cipher_suite.get_code_str(),
                vulns=response.handshake.cipher_suite.get_vuln_str(),
            )

        return default

    def get_result(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Result: {ssl_vulnerability.description}"


class SnippetConstructorES(SnippetConstructor):
    # pylint: disable=no-self-use
    def get_target(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Objetivo: {ssl_vulnerability.get_context()}"

    def get_intention(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Intención: {ssl_vulnerability.get_intention(LocalesEnum.ES)}"

    def get_versions(self, ssl_vulnerability: SSLVulnerability) -> str:
        tls_vers = ssl_vulnerability.get_context().get_supported_tls_versions()
        versions = ", ".join([ssl_id2ssl_name(v_id) for v_id in tls_vers])
        return f"Versiones de TLS en el servidor: {versions}"

    def get_request(self, ssl_vulnerability: SSLVulnerability) -> str:
        ssl_settings: SSLSettings = ssl_vulnerability.ssl_settings

        return (
            "Petición:\n"
            "    Fallback scsv: {scsv}\n"
            "    Versión TLS: {tls_version}"
            "    Intercambio de llaves: {key_exchange}\n"
            "    Autenticación: {authentication}\n"
            "    Encriptado: {cipher}\n"
            "    Hash: {ssl_hash}"
        ).format(
            scsv=ssl_settings.scsv,
            tls_version=ssl_id2ssl_name(ssl_settings.tls_version),
            key_exchange=", ".join(ssl_settings.key_exchange_names),
            authentication=", ".join(ssl_settings.authentication_names),
            cipher=", ".join(ssl_settings.cipher_names),
            ssl_hash=", ".join(ssl_settings.hash_names),
        )

    def get_response(self, ssl_vulnerability: SSLVulnerability) -> str:
        response = ssl_vulnerability.server_response
        default = "Respuesta:\n    ---"

        if response is None:
            return default

        if response.alert is not None:
            return (
                "Respuesta:\n"
                "    Tipo: ALERT\n"
                "    Nivel: {level}\n"
                "    Descripción: {description}"
            ).format(
                level=response.alert.level.name,
                description=response.alert.description.name,
            )

        if response.handshake is not None:
            return (
                "Respuesta:\n"
                "    Versión: {version}\n"
                "    Suite de cifrado seleccionada:\n"
                "        Nombre iana: {iana_name}\n"
                "        Nombre openssl: {openssl_name}\n"
                "        Código: {code}\n"
                "        Vulnerabilidades: {vulns}"
            ).format(
                version=ssl_id2ssl_name(response.handshake.version_id),
                iana_name=response.handshake.cipher_suite.iana_name,
                openssl_name=response.handshake.cipher_suite.openssl_name,
                code=response.handshake.cipher_suite.get_code_str(),
                vulns=response.handshake.cipher_suite.get_vuln_str(),
            )

        return default

    def get_result(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Resultado: {ssl_vulnerability.description}"


SnippetConstructors: Dict[LocalesEnum, SnippetConstructor] = {
    LocalesEnum.EN: SnippetConstructorEN(),
    LocalesEnum.ES: SnippetConstructorES(),
}


def snippet(
    locale: LocalesEnum,
    ssl_vulnerability: SSLVulnerability,
    columns_per_line: int = SNIPPETS_COLUMNS,
) -> str:
    return make_snippet(
        content=SnippetConstructors[locale].construct(ssl_vulnerability),
        viewport=SnippetViewport(
            column=0,
            wrap=True,
            columns_per_line=columns_per_line,
            line=ssl_vulnerability.get_line(),
        ),
    )
