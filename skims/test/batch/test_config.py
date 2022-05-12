from batch import (
    config,
)
from model.core_model import (
    FindingEnum,
    LocalesEnum,
    SkimsAPKConfig,
    SkimsConfig,
    SkimsHttpConfig,
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
    expected = [
        ("app.fluidattacks.com", "3000"),
        ("fluidattacks.com", "443"),
        ("app.fluidattacks.com", "443"),
        ("app.fluidattacks.com", "8001"),
    ]
    result = config.get_ssl_targets(urls)
    assert expected == result


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
@pytest.mark.usefixtures("test_integrates_session")
async def test_get_scopes_from_group(test_group: str) -> None:
    expected = {
        "https://fluidattacks.com/",
        "https://app.fluidattacks.com/",
    }
    result = await config.get_scopes_from_group(test_group, "namespace")
    assert expected == result


@pytest.mark.asyncio
@pytest.mark.skims_test_group("functional")
async def test_generate_config(test_group: str) -> None:
    expected = SkimsConfig(
        apk=SkimsAPKConfig(
            exclude=(),
            include=("glob(**/*.apk)",),
        ),
        checks=({FindingEnum.F001, FindingEnum.F008}),
        group=test_group,
        http=SkimsHttpConfig(
            include=(
                "http://app.fluidattacks.com/",
                "http://fluidattacks.com/",
                "https://app.fluidattacks.com/",
                "https://fluidattacks.com/",
            ),
        ),
        language=LocalesEnum.EN,
        namespace="namespace",
        output=os.path.abspath("result.csv"),
        path=SkimsPathConfig(
            include=(".",),
            exclude=("glob(**/.git)",),
            lib_path=True,
            lib_root=True,
        ),
        ssl=SkimsSslConfig(
            include=(
                SkimsSslTarget(host="fluidattacks.com", port=443),
                SkimsSslTarget(host="app.fluidattacks.com", port=443),
            )
        ),
        start_dir=os.getcwd(),
        working_dir=os.path.abspath("."),
    )
    result = await config.generate_config(
        group_name=test_group,
        namespace="namespace",
        language=LocalesEnum.EN,
        working_dir=".",
        checks=("F001", "F008"),
    )
    assert expected.checks == result.checks
    assert expected.http == result.http
    assert expected.ssl == result.ssl
