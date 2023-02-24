from dataloaders import (
    get_new_context,
)
from db_model.groups.types import (
    GroupUnreliableIndicators,
)
from db_model.types import (
    CodeLanguage,
)
from decimal import (
    Decimal,
)
import os
import pytest
from schedulers.groups_languages_distribution import (
    main as update_language_indicators,
)
from typing import (
    Any,
)
from unittest import (
    mock,
)


def clone_test_repository(
    tmpdir: str,
    group_name: str,
    optional_repo_nickname: str | None,  # pylint: disable=unused-argument
) -> Any:
    fusion_path: str = os.path.join(
        tmpdir, "groups", group_name, "fusion", "nickname1"
    )
    os.makedirs(name=fusion_path, exist_ok=True)
    with open(
        os.path.join(fusion_path, "file.py"), "w", encoding="utf-8"
    ) as python_file:
        python_file.write('import os\n\n\n# Test\nprint("Hello World!")\n')
    return mock.DEFAULT


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("groups_languages_distribution")
async def test_update_groups_languages(populate: bool) -> None:
    assert populate

    group_name = "test_group_1"
    loaders = get_new_context()
    group_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    assert group_indicators.closed_vulnerabilities == 10
    assert group_indicators.code_languages is None
    assert group_indicators.max_severity == Decimal("8.0")

    with mock.patch(
        target="schedulers.groups_languages_distribution.pull_repositories",
        side_effect=clone_test_repository,
    ):
        await update_language_indicators()

    loaders.group_unreliable_indicators.clear(group_name)
    group_new_indicators: GroupUnreliableIndicators = (
        await loaders.group_unreliable_indicators.load(group_name)
    )
    assert group_new_indicators.closed_vulnerabilities == 10
    assert group_new_indicators.code_languages == [
        CodeLanguage(language="Python", loc=3)
    ]
    assert group_new_indicators.max_severity == Decimal("8.0")
