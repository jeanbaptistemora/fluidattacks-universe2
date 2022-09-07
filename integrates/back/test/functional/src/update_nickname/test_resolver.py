# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from . import (
    get_finding,
    put_mutation,
)
from batch import (
    dal as batch_dal,
)
from batch.actions import (
    update_nickname,
)
from batch.enums import (
    Action,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
import json
import pytest
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_nickname")
async def test_should_update_successfully(populate: bool) -> None:
    assert populate

    batch_actions = await batch_dal.get_actions()
    actions_by_name = {
        Action[action.action_name.upper()]: action for action in batch_actions
    }
    assert len(batch_actions) == 1
    assert Action.UPDATE_NICKNAME in actions_by_name

    loaders: Dataloaders = get_new_context()
    root_vulns: tuple[Vulnerability, ...] = tuple(
        sorted(
            await loaders.root_vulnerabilities.load(
                "88637616-41d4-4242-854a-db8ff7fe1ab6"
            )
        )
    )
    await update_unreliable_indicators_by_deps(
        EntityDependency.upload_file,
        finding_ids=[root_vulns[0].finding_id],
        vulnerability_ids=[root_vulns[0].id, root_vulns[1].id],
    )
    finding: Finding = await loaders.finding.load(root_vulns[0].finding_id)

    assert not root_vulns[0].where.startswith("test123/")
    assert root_vulns[0].where.startswith("test/")
    assert root_vulns[1].where.startswith("test/")
    assert root_vulns[0].where == "test/data/lib_path/f050/csharp.cs"
    assert root_vulns[1].where == "test/data/lib_path/f060/csharp.cs"
    assert (
        finding.unreliable_indicators.unreliable_where
        == f"192.168.1.20, {root_vulns[0].where}, {root_vulns[1].where}"
    )

    loaders.root_vulnerabilities.clear_all()
    loaders.finding.clear_all()
    await update_nickname.update_nickname(
        item=actions_by_name[Action.UPDATE_NICKNAME]
    )
    root_vulns_updated: tuple[Vulnerability, ...] = tuple(
        sorted(
            await loaders.root_vulnerabilities.load(
                "88637616-41d4-4242-854a-db8ff7fe1ab6"
            )
        )
    )
    finding_updated: Finding = await loaders.finding.load(
        root_vulns_updated[0].finding_id
    )
    wheres_updated = [
        "192.168.1.20",
        root_vulns_updated[0].where,
        root_vulns_updated[1].where,
    ]

    assert not root_vulns_updated[0].where.startswith("test/")
    assert root_vulns_updated[0].where.startswith("test123/")
    assert root_vulns_updated[1].where.startswith("test123/")
    assert (
        root_vulns_updated[0].where == "test123/data/lib_path/f050/csharp.cs"
    )
    assert (
        root_vulns_updated[1].where == "test123/data/lib_path/f060/csharp.cs"
    )
    assert (
        finding_updated.unreliable_indicators.unreliable_where
        != f"192.168.1.20, {root_vulns[0].where}, {root_vulns[1].where}"
    )
    assert finding_updated.unreliable_indicators.unreliable_where == str.join(
        ", ", wheres_updated
    )


@pytest.mark.asyncio
@pytest.mark.resolver_test_group("update_nickname")
async def test_should_mutate_successfully(populate: bool) -> None:
    assert populate

    finding = await get_finding(
        finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
        user="test@fluidattacks.com",
    )
    vulnerabilities = [
        vuln["node"]
        for vuln in finding["data"]["finding"]["vulnerabilitiesConnection"][
            "edges"
        ]
    ]

    wheres = [
        vulnerabilities[0]["where"],
        vulnerabilities[1]["where"],
        vulnerabilities[2]["where"],
    ]

    assert finding["data"]["finding"]["where"] == str.join(", ", wheres)
    assert vulnerabilities[1]["where"].startswith("test123/")
    assert vulnerabilities[2]["where"].startswith("test123/")
    assert not vulnerabilities[0]["where"].startswith("test123/")

    result = await put_mutation(
        branch="development",
        environment="QA",
        gitignore=json.dumps(["node_modules/*"]),
        root_id="88637616-41d4-4242-854a-db8ff7fe1ab6",
        includes_health_check=True,
        nickname="groupnick",
        url="https://gitlab.com/fluidattacks/test",
        use_vpn=True,
        group_name="group123",
        user="test@fluidattacks.com",
    )

    assert "errors" not in result
    assert "success" in result["data"]["updateGitRoot"]
    assert result["data"]["updateGitRoot"]["success"]

    batch_actions = await batch_dal.get_actions()
    assert len(batch_actions) == 2

    actions_by_name = {
        Action[action.action_name.upper()]: action
        for action in batch_actions
        if action.key != "1"
    }
    assert Action.UPDATE_NICKNAME in actions_by_name

    await update_nickname.update_nickname(
        item=actions_by_name[Action.UPDATE_NICKNAME]
    )
    finding_updated = await get_finding(
        finding_id="918fbc15-2121-4c2a-83a8-dfa8748bcb2e",
        user="test@fluidattacks.com",
    )
    vulnerabilities_updated = [
        vuln["node"]
        for vuln in finding_updated["data"]["finding"][
            "vulnerabilitiesConnection"
        ]["edges"]
    ]
    wheres_updated = [
        vulnerabilities_updated[0]["where"],
        vulnerabilities_updated[1]["where"],
        vulnerabilities_updated[2]["where"],
    ]

    assert finding_updated["data"]["finding"]["where"] == str.join(
        ", ", wheres_updated
    )
    assert vulnerabilities_updated[1]["where"].startswith("groupnick/")
    assert vulnerabilities_updated[2]["where"].startswith("groupnick/")
    assert not vulnerabilities_updated[0]["where"].startswith("groupnick/")

    batch_actions = await batch_dal.get_actions()
    assert len(batch_actions) == 1
