from db_model.findings.types import (
    Finding,
)
from reports.certificate import (
    CertificateCreator,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Any,
    Tuple,
)


async def generate_cert_file(
    *,
    loaders: Any,
    description: str,
    findings_ord: Tuple[Finding, ...],
    group_name: str,
    lang: str,
) -> str:
    with TemporaryDirectory() as tempdir:
        pdf_maker = CertificateCreator(lang, "cert", tempdir)
        await pdf_maker.cert(
            findings_ord,
            group_name,
            description,
            loaders,
        )
    return pdf_maker.out_name
