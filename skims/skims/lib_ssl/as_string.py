from lib_ssl.types import (
    SSLVersionId,
    SSLVersionName,
    SSLVulnerability,
)
from model.core_model import (
    LocalesEnum,
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


def get_snippet_skeleton_en() -> str:
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


def get_snippet_skeleton_es() -> str:
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


def snippet(
    locale: LocalesEnum,
    ssl_vulnerability: SSLVulnerability,
    columns_per_line: int = SNIPPETS_COLUMNS,
) -> str:

    ssl_settings = ssl_vulnerability.ssl_settings
    snippet_skeleton: str = ""

    if locale == LocalesEnum.ES:
        snippet_skeleton = get_snippet_skeleton_es()
    else:
        snippet_skeleton = get_snippet_skeleton_en()

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
