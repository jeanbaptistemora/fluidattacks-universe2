from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
import asyncio
from back.tests.unit.utils import (
    create_dummy_session,
)
from batch.dal import (
    get_actions,
)
from batch.types import (
    BatchProcessing,
)
from context import (
    STARTDIR,
)
from dataloaders import (
    apply_context_attrs,
)
import os
import pytest
import subprocess
from typing import (
    List,
)

pytestmark = pytest.mark.asyncio


async def _get_batch_job(*, entity: str) -> BatchProcessing:
    all_actions = await get_actions()
    return next((action for action in all_actions if action.entity == entity))


async def _run(*, entity: str, additional_info: str) -> int:
    batch_action = await _get_batch_job(entity=entity)
    cmd_args: List[str] = [
        "test",
        os.environ["API_STATUS"],
        "report",
        entity,
        batch_action.subject,
        batch_action.time,
        additional_info,
    ]
    process: asyncio.subprocess.Process = await asyncio.create_subprocess_exec(
        os.environ["BATCH_BIN"],
        *cmd_args,
        stdin=subprocess.DEVNULL,
    )

    return await process.wait()


async def test_finding_report() -> None:
    query_pdf = """
        query test {
            report(
                groupName: "oneshottest",
                reportType: PDF,
                lang: EN) {
                url
            }
        }
    """
    query_xls = """
        query test {
            report(
                groupName: "oneshottest",
                reportType: XLS) {
                url
            }
        }
    """
    query_data = """
        query test {
            report(
                groupName: "oneshottest",
                reportType: DATA) {
                url
            }
        }
    """
    data_pdf = {"query": query_pdf}
    data_xls = {"query": query_xls}
    data_data = {"query": query_data}
    request = await create_dummy_session("integratesmanager@gmail.com")
    request = apply_context_attrs(request)
    _, result_pdf = await graphql(SCHEMA, data_pdf, context_value=request)
    _, result_xls = await graphql(SCHEMA, data_xls, context_value=request)
    _, result_data = await graphql(SCHEMA, data_data, context_value=request)
    assert all(
        "url" in result["data"]["report"] and result["data"]["report"]["url"]
        for result in [result_xls, result_data, result_pdf]
    )
    assert (
        await _run(
            entity="oneshottest",
            additional_info="DATA",
        )
        == 0
    )


def test_pdf_paths() -> None:
    # secure_pdf.py paths
    base = f"{STARTDIR}/integrates/back/src/reports"
    secure_pdf_paths = [
        base,
        f"{base}/results/results_pdf/",
        f"{base}/resources/themes/watermark_integrates_en.pdf",
        f"{base}/resources/themes/overlay_footer.pdf",
    ]

    for path in secure_pdf_paths:
        assert os.path.exists(path), f"path: {path} is not valid"

    # pdf.py paths
    path = f"{STARTDIR}/integrates/back/src/reports"
    pdf_paths = [
        path,
        f"{path}/resources/fonts",
        f"{path}/resources/themes",
        f"{path}/results/results_pdf/",
        f"{path}/templates/pdf/executive_new.adoc",
        f"{path}/templates/pdf/tech_new.adoc",
        f"{path}/tpls/",
    ]

    for path in pdf_paths:
        assert os.path.exists(path), f"path: {path} is not valid"
