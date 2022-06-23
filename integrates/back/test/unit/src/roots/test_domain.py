from dataloaders import (
    get_new_context,
)
import pytest
from roots import (
    domain as roots_domain,
)

# Constants
pytestmark = [
    pytest.mark.asyncio,
]


async def test_get_root_id_by_nickname() -> None:
    loaders = get_new_context()
    group_name = "unittesting"
    group_roots_loader = loaders.group_roots
    group_roots = await group_roots_loader.load(group_name)
    root_id = roots_domain.get_root_id_by_nickname(
        "product", group_roots, only_git_roots=True
    )
    assert root_id == "4039d098-ffc5-4984-8ed3-eb17bca98e19"


async def test_get_last_cloning_successful() -> None:
    loaders = get_new_context()
    root_id = "4039d098-ffc5-4984-8ed3-eb17bca98e19"
    item = await roots_domain.get_last_cloning_successful(loaders, root_id)
    assert item.status == "OK"


@pytest.mark.parametrize(
    "url_input,expected",
    [
        (
            "https://mycompany@dev.azure.com/"
            "mycompany/myproject/_git/myproject",
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
        ),
        (
            "https://mycompany@dev.azure.com:30/"
            "mycompany/myproject/_git/myproject",
            "https://dev.azure.com:30/mycompany/myproject/_git/myproject",
        ),
        (
            "ssh://git@ssh.dev.azure.com:v3/fluidattacks-product/demo/demo",
            "ssh://git@ssh.dev.azure.com:v3/fluidattacks-product/demo/demo",
        ),
        (
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
            "https://dev.azure.com/mycompany/myproject/_git/myproject",
        ),
    ],
)
def test_format_url(url_input: str, expected: str) -> None:
    assert roots_domain.format_git_repo_url(url_input) == expected
