# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from back.src.settings.logger import (
    LOGGING,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
import jinja2
from jinja2.utils import (
    select_autoescape,
)
import logging
import matplotlib
from reports.pdf import (
    CreatorPdf,
)
import subprocess  # nosec
from typing import (
    TypedDict,
)

logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
StandardReportContext = TypedDict(
    "StandardReportContext",
    {
        "group_name": str,
        "words": dict[str, str],
    },
)


class StandardReportCreator(CreatorPdf):
    """Class to generate standards report in PDF."""

    standard_report_context: StandardReportContext

    def __init__(  # pylint: disable=too-many-arguments
        self, lang: str, doctype: str, tempdir: str, group: str, user: str
    ) -> None:
        "Class constructor"
        super().__init__(lang, doctype, tempdir, group, user)
        self.proj_tpl = f"templates/pdf/unfulfilled_standards_{lang}.adoc"

    async def fill_context(
        self,
        group_name: str,
        loaders: Dataloaders,
    ) -> None:
        """Fetch information and fill out the context."""
        words = self.wordlist[self.lang]
        group: Group = await loaders.group.load(group_name)
        self.standard_report_context = {
            "group_name": group.name,
            "words": words,
        }

    async def unfulfilled_standards(
        self,
        group_name: str,
        loaders: Dataloaders,
    ) -> None:
        """Create the template to render and apply the context."""
        await self.fill_context(group_name, loaders)
        self.out_name = "unfulfilled_standards.pdf"
        template_loader = jinja2.FileSystemLoader(searchpath=self.path)
        template_env = jinja2.Environment(
            loader=template_loader,
            autoescape=select_autoescape(["html", "xml"], default=True),
        )
        template = template_env.get_template(self.proj_tpl)
        tpl_name = f"{self.tpl_dir}{group_name}_UN_STANDARDS.tpl"
        render_text = template.render(self.standard_report_context)
        with open(tpl_name, "wb") as tplfile:
            tplfile.write(render_text.encode("utf-8"))
        self.create_command(tpl_name, self.out_name)
        subprocess.call(self.command, shell=True)  # nosec
