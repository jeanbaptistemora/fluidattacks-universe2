# pylint: disable=import-error, too-many-locals
from api.schema import (
    SCHEMA,
)
from ariadne import (
    graphql,
)
import asyncio
from back.test.unit.src.utils import (
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


async def _get_batch_job(
    *, entity: str, additional_info: str
) -> BatchProcessing:
    all_actions = await get_actions()
    return next(
        (
            action
            for action in all_actions
            if action.entity == entity
            and additional_info in action.additional_info
        )
    )


async def _run(*, entity: str, additional_info: str) -> int:
    batch_action = await _get_batch_job(
        entity=entity, additional_info=additional_info
    )
    cmd_args: List[str] = [
        "test",
        batch_action.key,
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
                lang: EN,
                verificationCode: "123"
            ) {
                success
            }
        }
    """
    query_xls = """
        query test {
            report(
                groupName: "oneshottest",
                reportType: XLS,
                treatments: [ACCEPTED],
                verificationCode: "123"
            ) {
                success
            }
        }
    """
    query_data = """
        query test {
            report(
                groupName: "oneshottest",
                reportType: DATA,
                verificationCode: "123"
            ) {
                success
            }
        }
    """
    unit_query_data = """
        query test {
            report(
                groupName: "unittesting",
                reportType: DATA,
                verificationCode: "123"
            ) {
                success
            }
        }
    """
    data_pdf = {"query": query_pdf}
    data_xls = {"query": query_xls}
    data_data = {"query": query_data}
    unit_data_data = {"query": unit_query_data}
    request = await create_dummy_session("integratesmanager@gmail.com")
    request = apply_context_attrs(request)
    _, result_pdf = await graphql(SCHEMA, data_pdf, context_value=request)
    _, result_xls = await graphql(SCHEMA, data_xls, context_value=request)
    _, result_data = await graphql(SCHEMA, data_data, context_value=request)
    _, unit_result_data = await graphql(
        SCHEMA, unit_data_data, context_value=request
    )
    assert all(
        "success" in result["data"]["report"]
        and result["data"]["report"]["success"]
        for result in [result_xls, result_data, result_pdf, unit_result_data]
    )
    assert (
        await _run(
            entity="oneshottest",
            additional_info="DATA",
        )
        == 0
    )
    assert (
        await _run(
            entity="unittesting",
            additional_info="DATA",
        )
        == 0
    )

    # after processing report should allow to request a new one
    new_query_data = """
        query test {
            report(
                groupName: "oneshottest",
                reportType: DATA,
                verificationCode: "123"
            ) {
                success
            }
        }
    """
    new_data_query = {"query": new_query_data}
    new_request = await create_dummy_session("integratesmanager@gmail.com")
    new_request = apply_context_attrs(new_request)
    _, new_result_data = await graphql(
        SCHEMA, new_data_query, context_value=new_request
    )

    assert "errors" not in new_result_data
    assert new_result_data["data"]["report"]["success"]


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
        f"{path}/templates/pdf/executive.adoc",
        f"{path}/templates/pdf/tech.adoc",
        f"{path}/tpls/",
    ]

    for path in pdf_paths:
        assert os.path.exists(path), f"path: {path} is not valid"
