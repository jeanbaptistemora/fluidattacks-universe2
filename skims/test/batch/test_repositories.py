# pylint: disable=import-outside-toplevel
from ctx import (
    NAMESPACES_FOLDER,
)
import os
from os.path import (
    exists as path_exists,
    join as path_join,
)
import pytest


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_pull_namespace_from_s3")
@pytest.mark.usefixtures("test_integrates_session")
@pytest.mark.skims_test_group("functional")
async def test_delete_out_of_scope_files(test_group: str) -> None:
    from batch import (
        repositories,
    )

    path_to_namespace = os.path.join(
        NAMESPACES_FOLDER, test_group, "namespace"
    )
    await repositories.delete_out_of_scope_files(test_group, "namespace")
    assert path_exists(path_join(path_to_namespace, "README.md"))
    assert path_exists(
        path_join(path_to_namespace, "front/components/user/index.js")
    )
    assert not path_exists(
        path_join(path_to_namespace, "/back/test/conftest.py")
    )
    assert not path_exists(
        path_join(path_to_namespace, "/back/test/controlles/test_user.py")
    )
