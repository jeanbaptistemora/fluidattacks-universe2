from aioextensions import (
    collect,
)
from custom_exceptions import (
    InvalidStandardId,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
    GroupUnreliableIndicators,
)
import jinja2
from jinja2.utils import (
    select_autoescape,
)
import logging
import matplotlib
from newutils.compliance import (
    get_compliance_file,
)
from newutils.findings import (
    get_requirements_file,
)
from reports.pdf import (
    CreatorPdf,
)
from reports.typing import (
    UnfulfilledRequirementInfo,
    UnfulfilledStandardInfo,
)
from settings.logger import (
    LOGGING,
)
import subprocess  # nosec
from typing import (
    Optional,
    TypedDict,
)
import uuid

logging.config.dictConfig(LOGGING)  # NOSONAR
matplotlib.use("Agg")


# Constants
LOGGER = logging.getLogger(__name__)
StandardReportContext = TypedDict(
    "StandardReportContext",
    {
        "fluid_tpl": dict[str, str],
        "group_name": str,
        "has_unfulfilled_standards": bool,
        "unfulfilled_standards_to_display": list[UnfulfilledStandardInfo],
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
        lang: str,
        loaders: Dataloaders,
        selected_unfulfilled_standards: Optional[set[str]] = None,
    ) -> None:
        """Fetch information and fill out the context."""
        group: Group = await loaders.group.load(group_name)
        words = self.wordlist[lang]
        fluid_tpl_content = self.make_content(words)
        group_indicators: GroupUnreliableIndicators = (
            await loaders.group_unreliable_indicators.load(group_name)
        )
        compliance_file, requirements_file = await collect(
            (get_compliance_file(), get_requirements_file())
        )
        unfulfilled_standards_to_display = sorted(
            [
                UnfulfilledStandardInfo(
                    standard_id=unfulfilled_standard.name,
                    title=str(
                        compliance_file[unfulfilled_standard.name]["title"]
                    ).upper(),
                    summary=compliance_file[unfulfilled_standard.name][lang][
                        "summary"
                    ],
                    unfulfilled_requirements=[
                        UnfulfilledRequirementInfo(
                            id=requirement_id,
                            title=requirements_file[requirement_id][lang][
                                "title"
                            ],
                            description=requirements_file[requirement_id][
                                lang
                            ]["description"],
                        )
                        for requirement_id in (
                            unfulfilled_standard.unfulfilled_requirements
                        )
                    ],
                )
                for unfulfilled_standard in (
                    group_indicators.unfulfilled_standards
                )
                or []
            ],
            key=lambda standard: standard.title,
        )
        if selected_unfulfilled_standards is not None:
            if len(
                selected_unfulfilled_standards & compliance_file.keys()
            ) != len(selected_unfulfilled_standards):
                raise InvalidStandardId()

            unfulfilled_standards_to_display = [
                unfulfilled_standard_info
                for unfulfilled_standard_info in (
                    unfulfilled_standards_to_display
                )
                if unfulfilled_standard_info.standard_id
                in selected_unfulfilled_standards
            ]

        has_unfulfilled_standards = bool(
            group_indicators.unfulfilled_standards
        )
        self.standard_report_context = {
            "fluid_tpl": fluid_tpl_content,
            "group_name": group.name,
            "has_unfulfilled_standards": has_unfulfilled_standards,
            "unfulfilled_standards_to_display": (
                unfulfilled_standards_to_display
            ),
            "words": words,
        }

    async def unfulfilled_standards(
        self,
        loaders: Dataloaders,
        group_name: str,
        lang: str,
        unfulfilled_standards: Optional[set[str]] = None,
    ) -> None:
        """Create the template to render and apply the context."""
        await self.fill_context(
            group_name, lang, loaders, unfulfilled_standards
        )
        self.out_name = f"{str(uuid.uuid4())}.pdf"
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
