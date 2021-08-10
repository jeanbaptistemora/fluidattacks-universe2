from lib_ssl.suites import (
    SSLVersionId,
    SSLVersionName,
)
from lib_ssl.types import (
    SSLContext,
    SSLServerResponse,
    SSLSettings,
    SSLVulnerability,
)
from model.core_model import (
    LocalesEnum,
)
from typing import (
    Optional,
    Tuple,
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


def get_information_skeleton_en() -> str:
    content = "    available versions: {versions}\n"
    return content


def get_request_skeleton_en() -> str:
    content = "    fallback scsv: {scsv}\n"
    content += "    min version: {min_version}\n"
    content += "    max version: {max_version}\n"
    return content


def get_good_response_skeleton_en() -> str:
    content = "    version: {version}\n"
    content += "    Selected cipher suite:\n"
    content += "        iana name: {iana_name}\n"
    content += "        openssl name: {openssl_name}\n"
    content += "        code: {code}\n"
    content += "        vulnerabilities: {vulns}\n"
    return content


def get_bad_response_skeleton_en() -> str:
    content = "    type: ALERT\n"
    content += "    level: {level}\n"
    content += "    description: {description}\n"
    return content


def get_snippet_skeleton_en() -> str:
    content = "Target\n"
    content += "    {host}:{port}\n"
    content += "Intention\n"
    content += "    {intention}\n"
    content += "Information\n"
    content += "{information}"
    content += "Request\n"
    content += "{request}"
    content += "Response\n"
    content += "{response}"
    content += "Result\n"
    content += "    {result}\n"
    return content


def get_information_skeleton_es() -> str:
    content = "    versiones disponibles: {versions}\n"
    return content


def get_request_skeleton_es() -> str:
    content = "    fallback scsv: {scsv}\n"
    content += "    min versión: {min_version}\n"
    content += "    max versión: {max_version}\n"
    return content


def get_good_response_skeleton_es() -> str:
    content = "    versión: {version}\n"
    content += "    suite de cifrado:\n"
    content += "        nombre iana: {iana_name}\n"
    content += "        nombre openssl: {openssl_name}\n"
    content += "        código: {code}\n"
    content += "        vulnerabilidades: {vulns}\n"
    return content


def get_bad_response_skeleton_es() -> str:
    content = "    tipo: ALERT\n"
    content += "    nivel: {level}\n"
    content += "    descripción: {description}\n"
    return content


def get_snippet_skeleton_es() -> str:
    content = "Objetivo\n"
    content += "    {host}:{port}\n"
    content += "Intención\n"
    content += "    {intention}\n"
    content += "Información\n"
    content += "{information}"
    content += "Petición\n"
    content += "{request}"
    content += "Respuesta\n"
    content += "{response}"
    content += "Resultado\n"
    content += "    {result}\n"
    return content


def snippet(
    locale: LocalesEnum,
    ssl_vulnerability: SSLVulnerability,
    columns_per_line: int = SNIPPETS_COLUMNS,
) -> str:

    # pylint: disable=too-many-locals
    ssl_settings: SSLSettings = ssl_vulnerability.ssl_settings
    context: SSLContext = ssl_vulnerability.ssl_settings.context
    tls_vers: Tuple[SSLVersionId, ...] = context.get_supported_tls_versions()
    s_response: Optional[SSLServerResponse] = ssl_vulnerability.server_response

    if locale == LocalesEnum.ES:
        information_skeleton = get_information_skeleton_es()
        request_skeleton = get_request_skeleton_es()
        bad_response_skeleton = get_bad_response_skeleton_es()
        good_response_skeleton = get_good_response_skeleton_es()
        snippet_skeleton = get_snippet_skeleton_es()
    else:
        information_skeleton = get_information_skeleton_en()
        request_skeleton = get_request_skeleton_en()
        bad_response_skeleton = get_bad_response_skeleton_en()
        good_response_skeleton = get_good_response_skeleton_en()
        snippet_skeleton = get_snippet_skeleton_en()

    information: str = "    ---\n"
    if len(tls_vers) > 0:
        information = information_skeleton.format(
            versions=", ".join([ssl_id2ssl_name(v_id) for v_id in tls_vers])
        )

    request: str = request_skeleton.format(
        scsv=ssl_settings.scsv,
        min_version=ssl_id2ssl_name(ssl_settings.min_version),
        max_version=ssl_id2ssl_name(ssl_settings.max_version),
    )

    response: str = "    ---\n"
    if s_response is not None:
        if s_response.alert is not None:
            response = bad_response_skeleton.format(
                level=s_response.alert.level.name,
                description=s_response.alert.description.name,
            )
        elif s_response.handshake is not None:
            response = good_response_skeleton.format(
                version=ssl_id2ssl_name(s_response.handshake.version_id),
                iana_name=s_response.handshake.cipher_suite.iana_name,
                openssl_name=s_response.handshake.cipher_suite.openssl_name,
                code=s_response.handshake.cipher_suite.get_code_str(),
                vulns=s_response.handshake.cipher_suite.get_vuln_str(),
            )

    content: str = snippet_skeleton.format(
        host=ssl_settings.context.host,
        port=ssl_settings.context.port,
        intention=ssl_settings.intention[locale],
        information=information,
        request=request,
        response=response,
        result=ssl_vulnerability.description,
    )

    return make_snippet(
        content=content,
        viewport=SnippetViewport(
            column=0,
            wrap=True,
            columns_per_line=columns_per_line,
            line=ssl_vulnerability.get_line(),
        ),
    )
