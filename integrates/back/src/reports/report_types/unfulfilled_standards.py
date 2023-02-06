from dataloaders import (
    Dataloaders,
)
import logging
import logging.config
from reports.secure_pdf import (
    SecurePDF,
)
from reports.standard_report import (
    StandardReportCreator,
)
from settings import (
    LOGGING,
)
from tempfile import (
    TemporaryDirectory,
)
from typing import (
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def generate_pdf_file(
    *,
    loaders: Dataloaders,
    group_name: str,
    stakeholder_email: str,
    unfulfilled_standards: Optional[set[str]] = None,
) -> str:
    # The standard file is only available in English
    lang = "en"
    secure_pdf = SecurePDF()
    report_filename = ""
    with TemporaryDirectory() as tempdir:
        pdf_maker = StandardReportCreator(
            lang,
            "unfulfilled_standards",
            tempdir,
            group_name,
            stakeholder_email,
        )
        await pdf_maker.unfulfilled_standards(
            loaders,
            group_name,
            lang,
            unfulfilled_standards=unfulfilled_standards,
        )
    report_filename = await secure_pdf.create_full(
        loaders, stakeholder_email, pdf_maker.out_name, group_name
    )

    return report_filename
