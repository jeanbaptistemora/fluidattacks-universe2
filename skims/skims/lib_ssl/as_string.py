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
    # pylint: disable=unused-argument
    # pylint: disable=no-self-use
    def get_server(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Server: ---"

    def get_versions(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "Available TLS versions: ---"

    def get_intention_title(self) -> str:
        return "------------------------- Intention --------------------------"

    def get_intention(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "NONE"

    def get_request_title(self) -> str:
        return "-------------------------- Request ---------------------------"

    def get_request(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "NONE"

    def get_response_title(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "-------------------------- Response --------------------------"

    def get_response(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "NONE"

    def get_conclusion_title(self) -> str:
        return "------------------------- Conclusion -------------------------"

    def get_conclusion(self, ssl_vulnerability: SSLVulnerability) -> str:
        return "NONE"

    def construct(self, ssl_vulnerability: SSLVulnerability) -> str:
        return (
            "{server}\n"
            "{versions}\n"
            "{intention_title}\n"
            "{intention}\n"
            "{request_title}\n"
            "{request}\n"
            "{response_title}\n"
            "{response}\n"
            "{conclusion_title}\n"
            "{conclusion}\n"
        ).format(
            server=self.get_server(ssl_vulnerability),
            versions=self.get_versions(ssl_vulnerability),
            intention_title=self.get_intention_title(),
            intention=self.get_intention(ssl_vulnerability),
            request_title=self.get_request_title(),
            request=self.get_request(ssl_vulnerability),
            response_title=self.get_response_title(ssl_vulnerability),
            response=self.get_response(ssl_vulnerability),
            conclusion_title=self.get_conclusion_title(),
            conclusion=self.get_conclusion(ssl_vulnerability),
        )


class SnippetConstructorEN(SnippetConstructor):
    # pylint: disable=no-self-use
    def get_server(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Server: {ssl_vulnerability.get_context()}"

    def get_versions(self, ssl_vulnerability: SSLVulnerability) -> str:
        tls_vers = ssl_vulnerability.get_context().get_supported_tls_versions()
        versions = ", ".join([ssl_id2ssl_name(v_id) for v_id in tls_vers])
        return f"Available TLS versions: {versions}"

    def get_intention_title(self) -> str:
        return (
            "-------------------------------"
            "Intention"
            "-------------------------------"
        )

    def get_intention(self, ssl_vulnerability: SSLVulnerability) -> str:
        return ssl_vulnerability.get_intention(LocalesEnum.EN)

    def get_request_title(self) -> str:
        return (
            "--------------"
            "Request made with the following parameters"
            "---------------"
        )

    def get_request(self, ssl_vulnerability: SSLVulnerability) -> str:
        ssl_settings: SSLSettings = ssl_vulnerability.ssl_settings

        return (
            "TLS version: {tls_version}\n"
            "Key exchange: {key_exchange}\n"
            "Authentication: {authentication}\n"
            "Cipher: {cipher}\n"
            "Hash: {ssl_hash}"
        ).format(
            tls_version=ssl_id2ssl_name(ssl_settings.tls_version),
            key_exchange=", ".join(ssl_settings.key_exchange_names),
            authentication=", ".join(ssl_settings.authentication_names),
            cipher=", ".join(ssl_settings.cipher_names),
            ssl_hash=", ".join(ssl_settings.hash_names),
        )

    def get_response_title(self, ssl_vulnerability: SSLVulnerability) -> str:
        return (
            "---------------------"
            "Response obtained from server"
            "---------------------"
        )

    def get_response(self, ssl_vulnerability: SSLVulnerability) -> str:
        response = ssl_vulnerability.server_response

        if response is None:
            return "Result: UNSUCCESSFULL_CONNECTION"

        if response.alert is not None:
            return (
                "Result: CONNECTION_FAILED\n"
                "Type: ALERT\n"
                "Level: {level}\n"
                "Description: {description}"
            ).format(
                level=response.alert.level.name,
                description=response.alert.description.name,
            )

        if response.handshake is not None:
            return (
                "Result: CONNECTION_SUCCESS\n"
                "TLS version: {version}\n"
                "Selected cipher suite: {iana}\n"
                "    Openssl name: {openssl}\n"
                "    Code: {code}\n"
                "    Vulnerabilities: {vulns}"
            ).format(
                version=ssl_id2ssl_name(response.handshake.version_id),
                iana=response.handshake.cipher_suite.iana_name,
                openssl=response.handshake.cipher_suite.get_openssl_name(),
                code=response.handshake.cipher_suite.get_code_str(),
                vulns=response.handshake.cipher_suite.get_vuln_str(),
            )

        return "NONE"

    def get_conclusion_title(self) -> str:
        return (
            "------------------------------"
            "Conclusion"
            "-------------------------------"
        )

    def get_conclusion(self, ssl_vulnerability: SSLVulnerability) -> str:
        return ssl_vulnerability.description


class SnippetConstructorES(SnippetConstructor):
    # pylint: disable=no-self-use
    def get_server(self, ssl_vulnerability: SSLVulnerability) -> str:
        return f"Servidor: {ssl_vulnerability.get_context()}"

    def get_versions(self, ssl_vulnerability: SSLVulnerability) -> str:
        tls_vers = ssl_vulnerability.get_context().get_supported_tls_versions()
        versions = ", ".join([ssl_id2ssl_name(v_id) for v_id in tls_vers])
        return f"Versiones de TLS disponibles en el servidor: {versions}"

    def get_intention_title(self) -> str:
        return (
            "-------------------------------"
            "Intención"
            "-------------------------------"
        )

    def get_intention(self, ssl_vulnerability: SSLVulnerability) -> str:
        return ssl_vulnerability.get_intention(LocalesEnum.ES)

    def get_request_title(self) -> str:
        return (
            "-----------"
            "Petición realizada con los siguientes parámetros"
            "------------"
        )

    def get_request(self, ssl_vulnerability: SSLVulnerability) -> str:
        ssl_settings: SSLSettings = ssl_vulnerability.ssl_settings

        return (
            "Versión TLS: {tls_version}\n"
            "Intercambio de llaves: {key_exchange}\n"
            "Autenticación: {authentication}\n"
            "Encriptado: {cipher}\n"
            "Hash: {ssl_hash}"
        ).format(
            tls_version=ssl_id2ssl_name(ssl_settings.tls_version),
            key_exchange=", ".join(ssl_settings.key_exchange_names),
            authentication=", ".join(ssl_settings.authentication_names),
            cipher=", ".join(ssl_settings.cipher_names),
            ssl_hash=", ".join(ssl_settings.hash_names),
        )

    def get_response_title(self, ssl_vulnerability: SSLVulnerability) -> str:
        return (
            "-----------------------------"
            "Respuesta obtenida del servidor"
            "------------------------------"
        )

    def get_response(self, ssl_vulnerability: SSLVulnerability) -> str:
        response = ssl_vulnerability.server_response

        if response is None:
            return "Resultado: UNSUCCESSFULL_CONNECTION"

        if response.alert is not None:
            return (
                "Resultado: CONNECTION_FAILED\n"
                "Tipo: ALERT\n"
                "Nivel: {level}\n"
                "Descripción: {description}"
            ).format(
                level=response.alert.level.name,
                description=response.alert.description.name,
            )

        if response.handshake is not None:
            return (
                "Resultado: CONNECTION_SUCCESS\n"
                "Versión TLS: {version}\n"
                "Suite de cifrado seleccionada: {iana}\n"
                "    Nombre openssl: {openssl}\n"
                "    Código: {code}\n"
                "    Vulnerabilidades: {vulns}"
            ).format(
                version=ssl_id2ssl_name(response.handshake.version_id),
                iana=response.handshake.cipher_suite.iana_name,
                openssl=response.handshake.cipher_suite.get_openssl_name(),
                code=response.handshake.cipher_suite.get_code_str(),
                vulns=response.handshake.cipher_suite.get_vuln_str(),
            )

        return "NONE"

    def get_conclusion_title(self) -> str:
        return (
            "------------------------------"
            "Conclusión"
            "-------------------------------"
        )

    def get_conclusion(self, ssl_vulnerability: SSLVulnerability) -> str:
        return ssl_vulnerability.description


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
            line=0,
            column=0,
            wrap=True,
            columns_per_line=columns_per_line,
        ),
    )
