# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def generate_pdf_file(
    *,
    loaders: Dataloaders,
    group_name: str,
    lang: str,
    user_email: str,
) -> str:
    secure_pdf = SecurePDF()
    report_filename = ""
    with TemporaryDirectory() as tempdir:
        pdf_maker = StandardReportCreator(
            lang, "unfulfilled_standards", tempdir, group_name, user_email
        )
        await pdf_maker.unfulfilled_standards(
            group_name,
            loaders,
        )
    report_filename = await secure_pdf.create_full(
        loaders, user_email, pdf_maker.out_name, group_name
    )

    return report_filename
