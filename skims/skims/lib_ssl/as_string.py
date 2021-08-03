from lib_ssl.types import (
    SSLServerResponse,
    SSLSettings,
    SSLVersionId,
    SSLVersionName,
    SSLVulnerability,
)
from model.core_model import (
    LocalesEnum,
)
from typing import (
    Optional,
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


def get_request_skeleton_en() -> str:
    content = "    fallback scsv: {scsv}\n"
    content += "    min version: {min_version}\n"
    content += "    max version: {max_version}\n"
    return content


def get_good_response_skeleton_en() -> str:
    content = "    cipher suite: {cipher_suite}\n"
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
    content += "Request\n"
    content += "{request}"
    content += "Response\n"
    content += "{response}"
    content += "Result\n"
    content += "    {result}\n"
    return content


def get_request_skeleton_es() -> str:
    content = "    fallback scsv: {scsv}\n"
    content += "    min versión: {min_version}\n"
    content += "    max versión: {max_version}\n"
    return content


def get_good_response_skeleton_es() -> str:
    content = "    suite de cifrado: {cipher_suite}\n"
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

    ssl_settings: SSLSettings = ssl_vulnerability.ssl_settings
    s_response: Optional[SSLServerResponse] = ssl_vulnerability.server_response

    if locale == LocalesEnum.ES:
        request_skeleton = get_request_skeleton_es()
        bad_response_skeleton = get_bad_response_skeleton_es()
        good_response_skeleton = get_good_response_skeleton_es()
        snippet_skeleton = get_snippet_skeleton_es()
    else:
        request_skeleton = get_request_skeleton_en()
        bad_response_skeleton = get_bad_response_skeleton_en()
        good_response_skeleton = get_good_response_skeleton_en()
        snippet_skeleton = get_snippet_skeleton_en()

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
                cipher_suite=s_response.handshake.cipher_suite.name,
            )

    content: str = snippet_skeleton.format(
        host=ssl_settings.context.host,
        port=ssl_settings.context.port,
        intention=ssl_settings.intention[locale],
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


def old_get_snippet_skeleton_en() -> str:
    content: str = "intention: {intention}\n"
    content += "SSL request made to {host}:{port} with following parameters\n"
    content += "   fallback scsv: {scsv}\n"
    content += "   min version: {min_version}\n"
    content += "   max version: {max_version}\n"
    content += "   ciphers: {ciphers}\n"
    content += "   mac: {mac}\n"
    content += "   key exchange: {key_exchange}\n"
    content += "result: {result}\n"
    return content


def old_get_snippet_skeleton_es() -> str:
    content: str = "intención: {intention}\n"
    content += "petición SSL hecha a {host}:{port} con los parámetros\n"
    content += "   fallback scsv: {scsv}\n"
    content += "   min versión: {min_version}\n"
    content += "   max versión: {max_version}\n"
    content += "   cifrados: {ciphers}\n"
    content += "   mac: {mac}\n"
    content += "   intercambio de llaves: {key_exchange}\n"
    content += "resultado: {result}\n"
    return content


def old_snippet(
    locale: LocalesEnum,
    ssl_vulnerability: SSLVulnerability,
    columns_per_line: int = SNIPPETS_COLUMNS,
) -> str:

    ssl_settings = ssl_vulnerability.ssl_settings
    snippet_skeleton: str = ""

    if locale == LocalesEnum.ES:
        snippet_skeleton = old_get_snippet_skeleton_es()
    else:
        snippet_skeleton = old_get_snippet_skeleton_en()

    content: str = snippet_skeleton.format(
        intention=ssl_settings.intention[locale],
        host=ssl_settings.context.host,
        port=ssl_settings.context.port,
        scsv=ssl_settings.scsv,
        min_version=ssl_id2ssl_name(ssl_settings.min_version),
        max_version=ssl_id2ssl_name(ssl_settings.max_version),
        ciphers=", ".join(ssl_settings.cipher_names),
        mac=", ".join(ssl_settings.mac_names),
        key_exchange=", ".join(ssl_settings.get_key_exchange_names()),
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
