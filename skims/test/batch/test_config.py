from batch import (
    config,
)
from integrates.dal import (
    get_group_roots,
)
from model.core_model import (
    FindingEnum,
    LocalesEnum,
    OutputFormat,
    SkimsAPKConfig,
    SkimsConfig,
    SkimsDastConfig,
    SkimsHttpConfig,
    SkimsOutputConfig,
    SkimsPathConfig,
    SkimsSslConfig,
    SkimsSslTarget,
)
import os
import pytest


@pytest.mark.skims_test_group("unittesting")
def test_get_urls_from_scopes() -> None:
    scopes = {"https://app.fluidattacks.com/", "https://fluidattacks.com/"}
    result = config.get_urls_from_scopes(scopes)
    expected = [
        "http://app.fluidattacks.com/",
        "http://fluidattacks.com/",
        "https://app.fluidattacks.com/",
        "https://fluidattacks.com/",
    ]
    assert expected == result


@pytest.mark.skims_test_group("unittesting")
def test_get_ssl_targets() -> None:
    urls = [
        "https://app.fluidattacks.com:3000/",
        "https://app.fluidattacks.com:8001/",
        "https://fluidattacks.com/",
        "https://app.fluidattacks.com/",
    ]
    expected = sorted(
        [
            ("app.fluidattacks.com", "3000"),
            ("fluidattacks.com", "443"),
            ("app.fluidattacks.com", "443"),
            ("app.fluidattacks.com", "8001"),
        ]
    )
    result = sorted(config.get_ssl_targets(urls))
    assert expected == result


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.skip(reason="Fixing")
@pytest.mark.usefixtures("test_integrates_session")
async def test_get_scopes_from_group(test_group: str) -> None:
    expected = {
        "https://fluidattacks.com/",
        "https://app.fluidattacks.com/",
    }
    result = await config.get_scopes_from_group(test_group, "static_namespace")
    assert expected == result


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.skip(reason="Fixing")
async def test_generate_config(test_group: str) -> None:
    expected = SkimsConfig(
        apk=SkimsAPKConfig(
            exclude=(),
            include=("glob(**/*.apk)",),
        ),
        checks=({FindingEnum.F001, FindingEnum.F008}),
        dast=SkimsDastConfig(
            aws_credentials=[],
            http=SkimsHttpConfig(
                include=(
                    "http://app.fluidattacks.com/",
                    "http://fluidattacks.com/",
                    "https://app.fluidattacks.com/",
                    "https://fluidattacks.com/",
                ),
            ),
            ssl=SkimsSslConfig(
                include=(
                    SkimsSslTarget(host="app.fluidattacks.com", port=443),
                    SkimsSslTarget(host="fluidattacks.com", port=443),
                )
            ),
        ),
        commit=None,
        group=test_group,
        language=LocalesEnum.EN,
        namespace="static_namespace",
        output=SkimsOutputConfig(
            file_path=os.path.abspath("result.csv"),
            format=OutputFormat.CSV,
        ),
        path=SkimsPathConfig(
            include=(".",),
            exclude=("glob(**/.git)",),
            lib_path=True,
            lib_root=True,
        ),
        start_dir=os.getcwd(),
        working_dir=os.path.abspath("."),
        execution_id=None,
    )
    git_root = next(
        (
            root
            for root in (await get_group_roots(group=test_group))
            if root.nickname == "static_namespace"
        )
    )
    result = await config.generate_config(
        group_name=test_group,
        git_root=git_root,
        language=LocalesEnum.EN,
        working_dir=".",
        checks=("F001", "F008"),
    )
    assert expected.checks == result.checks
    if expected.dast and result.dast:
        assert expected.dast.http == result.dast.http
        assert expected.dast.ssl == result.dast.ssl
