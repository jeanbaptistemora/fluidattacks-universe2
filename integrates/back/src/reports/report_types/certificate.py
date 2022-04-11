from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from reports.certificate import (
    CertificateCreator,
)
from reports.secure_pdf import (
    SecurePDF,
)
from tempfile import (
    TemporaryDirectory,
)


async def generate_cert_file(
    *,
    loaders: Dataloaders,
    description: str,
    findings_ord: tuple[Finding, ...],
    group_name: str,
    lang: str,
    user_email: str,
) -> str:
    secure_pdf = SecurePDF()
    report_filename = ""
    with TemporaryDirectory() as tempdir:
        pdf_maker = CertificateCreator(lang, "cert", tempdir)
        await pdf_maker.cert(
            findings_ord,
            group_name,
            description,
            loaders,
        )
    report_filename = await secure_pdf.create_full(
        user_email, pdf_maker.out_name, group_name
    )
    return report_filename
