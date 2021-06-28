from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from collections import (
    defaultdict,
)
from context import (
    FI_DB_MODEL_PATH,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
from dynamodb.table import (
    load_table,
)
from dynamodb.types import (
    GitRootCloning,
    GitRootItem,
    GitRootMetadata,
    GitRootState,
    GitRootToeInputItem,
    GitRootToeLinesItem,
    GroupMetadata,
    IPRootItem,
    IPRootMetadata,
    IPRootState,
    Item,
    OrgFindingPolicyItem,
    OrgFindingPolicyMetadata,
    OrgFindingPolicyState,
    PrimaryKey,
    RootItem,
    URLRootItem,
    URLRootMetadata,
    URLRootState,
    VulnerabilityItem,
    VulnerabilityMetadata,
    VulnerabilityState,
)
import json
from typing import (
    Optional,
    Tuple,
    Union,
)

with open(FI_DB_MODEL_PATH, mode="r") as file:
    TABLE = load_table(json.load(file))


def _build_root(
    *,
    group_name: str,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> RootItem:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=raw_items,
    )

    if metadata["type"] == "Git":
        cloning = historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="CLON",
            raw_items=raw_items,
        )

        return GitRootItem(
            cloning=GitRootCloning(
                modified_date=cloning["modified_date"],
                reason=cloning["reason"],
                status=cloning["status"],
            ),
            group_name=group_name,
            id=metadata[key_structure.sort_key].split("#")[1],
            metadata=GitRootMetadata(
                branch=metadata["branch"],
                type=metadata["type"],
                url=metadata["url"],
            ),
            state=GitRootState(
                environment_urls=state["environment_urls"],
                environment=state["environment"],
                gitignore=state["gitignore"],
                includes_health_check=state["includes_health_check"],
                modified_by=state["modified_by"],
                modified_date=state["modified_date"],
                nickname=state["nickname"],
                other=state.get("other"),
                reason=state.get("reason"),
                status=state["status"],
            ),
        )

    if metadata["type"] == "IP":
        return IPRootItem(
            group_name=group_name,
            id=metadata[key_structure.sort_key].split("#")[1],
            metadata=IPRootMetadata(
                address=metadata["address"],
                port=metadata["port"],
                type=metadata["type"],
            ),
            state=IPRootState(
                modified_by=state["modified_by"],
                modified_date=state["modified_date"],
                other=state.get("other"),
                reason=state.get("reason"),
                status=state["status"],
            ),
        )

    return URLRootItem(
        group_name=group_name,
        id=metadata[key_structure.sort_key].split("#")[1],
        metadata=URLRootMetadata(
            host=metadata["host"],
            path=metadata["path"],
            port=metadata["port"],
            protocol=metadata["protocol"],
            type=metadata["type"],
        ),
        state=URLRootState(
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            other=state.get("other"),
            reason=state.get("reason"),
            status=state["status"],
        ),
    )


async def get_root(
    *,
    group_name: str,
    root_id: str,
) -> Optional[RootItem]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name, "uuid": root_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["git_root_cloning"],
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_state"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    if results:
        return _build_root(
            group_name=group_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=results,
        )

    return None


async def get_roots(*, group_name: str) -> Tuple[RootItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": group_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["git_root_cloning"],
            TABLE.facets["git_root_metadata"],
            TABLE.facets["git_root_state"],
            TABLE.facets["ip_root_metadata"],
            TABLE.facets["ip_root_state"],
            TABLE.facets["url_root_metadata"],
            TABLE.facets["url_root_state"],
        ),
        index=index,
        table=TABLE,
    )

    root_items = defaultdict(list)
    for item in results:
        root_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        root_items[root_id].append(item)

    return tuple(
        _build_root(
            group_name=group_name,
            item_id=root_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for root_id, items in root_items.items()
    )


async def create_root(*, root: RootItem) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["git_root_metadata"],
        values={"name": root.group_name, "uuid": root.id},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(root.metadata._asdict()),
    }

    historic_state = historics.build_historic(
        attributes=dict(root.state._asdict()),
        historic_facet=TABLE.facets["git_root_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": root.state.modified_date,
            "name": root.group_name,
            "uuid": root.id,
        },
        latest_facet=TABLE.facets["git_root_state"],
    )

    items = (initial_metadata, *historic_state)

    if isinstance(root, GitRootItem):
        historic_cloning = historics.build_historic(
            attributes=dict(root.cloning._asdict()),
            historic_facet=TABLE.facets["git_root_historic_cloning"],
            key_structure=key_structure,
            key_values={
                "iso8601utc": root.cloning.modified_date,
                "name": root.group_name,
                "uuid": root.id,
            },
            latest_facet=TABLE.facets["git_root_cloning"],
        )
        await operations.batch_write_item(
            items=(*items, *historic_cloning), table=TABLE
        )
    else:
        await operations.batch_write_item(items=items, table=TABLE)


async def update_root_state(
    *,
    group_name: str,
    root_id: str,
    state: Union[GitRootState, IPRootState, URLRootState],
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(state._asdict()),
        historic_facet=TABLE.facets["git_root_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=TABLE.facets["git_root_state"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def update_git_root_cloning(
    *, cloning: GitRootCloning, group_name: str, root_id: str
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(cloning._asdict()),
        historic_facet=TABLE.facets["git_root_historic_cloning"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": cloning.modified_date,
            "name": group_name,
            "uuid": root_id,
        },
        latest_facet=TABLE.facets["git_root_cloning"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def create_git_root_toe_lines(
    *, root_toe_lines: GitRootToeLinesItem
) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_toe_lines"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": root_toe_lines.filename,
            "group_name": root_toe_lines.group_name,
            "root_id": root_toe_lines.root_id,
        },
    )
    toe_lines = {
        key_structure.partition_key: toe_lines_key.partition_key,
        key_structure.sort_key: toe_lines_key.sort_key,
        **dict(root_toe_lines._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=facet,
        item=toe_lines,
        table=TABLE,
    )


async def delete_git_root_toe_lines(
    *, filename: str, group_name: str, root_id: str
) -> None:
    facet = TABLE.facets["root_toe_lines"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": filename,
            "group_name": group_name,
            "root_id": root_id,
        },
    )
    await operations.delete_item(primary_key=toe_lines_key, table=TABLE)


def _build_git_root_toe_lines(
    *,
    group_name: str,
    key_structure: PrimaryKey,
    item: Item,
) -> GitRootToeLinesItem:
    sort_key_items = item[key_structure.sort_key].split("#", 4)
    root_id = sort_key_items[2]
    filename = sort_key_items[4]
    return GitRootToeLinesItem(
        comments=item["comments"],
        filename=filename,
        group_name=group_name,
        loc=item["loc"],
        modified_commit=item["modified_commit"],
        modified_date=item["modified_date"],
        root_id=root_id,
        tested_date=item["tested_date"],
        tested_lines=item["tested_lines"],
        sorts_risk_level=item["sorts_risk_level"],
    )


async def get_toe_lines_by_group(
    *, group_name: str
) -> Tuple[GitRootToeLinesItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_toe_lines"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    line_key = primary_key.sort_key.split("#")[0]
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(line_key)
        ),
        facets=(TABLE.facets["root_toe_lines"],),
        index=None,
        table=TABLE,
    )
    return tuple(
        _build_git_root_toe_lines(
            group_name=group_name, key_structure=key_structure, item=item
        )
        for item in results
    )


async def get_toe_lines_by_root(
    *, group_name: str, root_id: str
) -> Tuple[GitRootToeLinesItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_toe_lines"],
        values={"group_name": group_name, "root_id": root_id},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["root_toe_lines"],),
        table=TABLE,
    )
    return tuple(
        _build_git_root_toe_lines(
            group_name=group_name, key_structure=key_structure, item=item
        )
        for item in results
    )


async def update_git_root_toe_lines(
    *, root_toe_lines: GitRootToeLinesItem
) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_toe_lines"]
    toe_lines_key = keys.build_key(
        facet=facet,
        values={
            "filename": root_toe_lines.filename,
            "group_name": root_toe_lines.group_name,
            "root_id": root_toe_lines.root_id,
        },
    )
    toe_lines = {
        key_structure.partition_key: toe_lines_key.partition_key,
        key_structure.sort_key: toe_lines_key.sort_key,
        **dict(root_toe_lines._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=facet,
        item=toe_lines,
        table=TABLE,
    )


async def create_git_root_toe_input(
    *, root_toe_input: GitRootToeInputItem
) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_toe_input"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": root_toe_input.component,
            "entry_point": root_toe_input.entry_point,
            "group_name": root_toe_input.group_name,
        },
    )
    toe_input = {
        key_structure.partition_key: toe_input_key.partition_key,
        key_structure.sort_key: toe_input_key.sort_key,
        **dict(root_toe_input._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=facet,
        item=toe_input,
        table=TABLE,
    )


async def delete_git_root_toe_input(
    *,
    entry_point: str,
    component: str,
    group_name: str,
) -> None:
    facet = TABLE.facets["root_toe_input"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": component,
            "entry_point": entry_point,
            "group_name": group_name,
        },
    )
    await operations.delete_item(primary_key=toe_input_key, table=TABLE)


def _build_git_root_toe_input(
    *,
    group_name: str,
    item: Item,
) -> GitRootToeInputItem:
    return GitRootToeInputItem(
        commit=item["commit"],
        component=item["component"],
        created_date=item["created_date"],
        entry_point=item["entry_point"],
        group_name=group_name,
        seen_first_time_by=item["seen_first_time_by"],
        tested_date=item["tested_date"],
        verified=item["verified"],
        vulns=item["vulns"],
    )


async def get_toe_inputs_by_group(
    *, group_name: str
) -> Tuple[GitRootToeInputItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["root_toe_input"],
        values={"group_name": group_name},
    )
    key_structure = TABLE.primary_key
    inputs_key = primary_key.sort_key.split("#")[0]
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(inputs_key)
        ),
        facets=(TABLE.facets["root_toe_input"],),
        index=None,
        table=TABLE,
    )
    return tuple(
        _build_git_root_toe_input(group_name=group_name, item=item)
        for item in results
    )


async def update_git_root_toe_input(
    *, root_toe_input: GitRootToeInputItem
) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["root_toe_input"]
    toe_input_key = keys.build_key(
        facet=facet,
        values={
            "component": root_toe_input.component,
            "entry_point": root_toe_input.entry_point,
            "group_name": root_toe_input.group_name,
        },
    )
    toe_input = {
        key_structure.partition_key: toe_input_key.partition_key,
        key_structure.sort_key: toe_input_key.sort_key,
        **root_toe_input._asdict(),
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=facet,
        item=toe_input,
        table=TABLE,
    )


def _build_vuln(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> VulnerabilityItem:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=raw_items,
    )

    return VulnerabilityItem(
        id=metadata[key_structure.sort_key].split("#")[1],
        metadata=VulnerabilityMetadata(
            affected_components=metadata["affected_components"],
            attack_vector=metadata["attack_vector"],
            cvss=metadata["cvss"],
            cwe=metadata["cwe"],
            description=metadata["description"],
            evidences=metadata["evidences"],
            name=metadata["name"],
            recommendation=metadata["recommendation"],
            requirements=metadata["requirements"],
            source=metadata["source"],
            specific=metadata["specific"],
            threat=metadata["threat"],
            type=metadata["type"],
            using_sorts=metadata["using_sorts"],
            where=metadata["where"],
        ),
        state=VulnerabilityState(
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            reason=state["reason"],
            source=state["source"],
            status=state["status"],
            tags=state["tags"],
        ),
    )


async def get_vulnerability(
    *, root: GitRootItem, vuln_id: str
) -> Optional[VulnerabilityItem]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"root_uuid": root.id, "vuln_uuid": vuln_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["vulnerability_metadata"],
            TABLE.facets["vulnerability_state"],
        ),
        index=index,
        table=TABLE,
    )

    if results:
        return _build_vuln(
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=results,
        )

    return None


async def get_vulnerabilities(
    *, root: GitRootItem
) -> Tuple[VulnerabilityItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"root_uuid": root.id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["vulnerability_metadata"],
            TABLE.facets["vulnerability_state"],
        ),
        index=index,
        table=TABLE,
    )

    vuln_items = defaultdict(list)
    for item in results:
        vuln_id = "#".join(item[key_structure.sort_key].split("#")[:2])
        vuln_items[vuln_id].append(item)

    return tuple(
        _build_vuln(
            item_id=vuln_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for vuln_id, items in vuln_items.items()
    )


def _build_org_policy_finding(
    *,
    org_name: str,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> OrgFindingPolicyItem:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state = historics.get_latest(
        item_id=item_id,
        key_structure=key_structure,
        historic_suffix="STATE",
        raw_items=raw_items,
    )

    return OrgFindingPolicyItem(
        id=metadata[key_structure.sort_key].split("#")[1],
        org_name=org_name,
        metadata=OrgFindingPolicyMetadata(
            name=metadata["name"], tags=metadata.get("tags", {})
        ),
        state=OrgFindingPolicyState(
            modified_by=state["modified_by"],
            modified_date=state["modified_date"],
            status=state["status"],
        ),
    )


async def get_org_finding_policy(
    *,
    org_name: str,
    finding_policy_id: str,
) -> Optional[OrgFindingPolicyItem]:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": org_name, "uuid": finding_policy_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["org_finding_policy_metadata"],
            TABLE.facets["org_finding_policy_state"],
        ),
        index=index,
        table=TABLE,
    )

    if results:
        return _build_org_policy_finding(
            org_name=org_name,
            item_id=primary_key.partition_key,
            key_structure=key_structure,
            raw_items=results,
        )

    return None


async def get_org_finding_policies(
    *, org_name: str
) -> Tuple[OrgFindingPolicyItem, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": org_name},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["org_finding_policy_metadata"],
            TABLE.facets["org_finding_policy_state"],
        ),
        index=index,
        table=TABLE,
    )

    org_findings_policies_items = defaultdict(list)
    for item in results:
        finding_policy_id = "#".join(
            item[key_structure.sort_key].split("#")[:2]
        )
        org_findings_policies_items[finding_policy_id].append(item)

    return tuple(
        _build_org_policy_finding(
            org_name=org_name,
            item_id=finding_policy_id,
            key_structure=key_structure,
            raw_items=tuple(items),
        )
        for finding_policy_id, items in org_findings_policies_items.items()
    )


async def create_org_finding_policy(
    *, finding_policy: OrgFindingPolicyItem
) -> None:
    key_structure = TABLE.primary_key

    metadata_key = keys.build_key(
        facet=TABLE.facets["org_finding_policy_metadata"],
        values={"name": finding_policy.org_name, "uuid": finding_policy.id},
    )
    initial_metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(finding_policy.metadata._asdict()),
    }

    historic_state = historics.build_historic(
        attributes=dict(finding_policy.state._asdict()),
        historic_facet=TABLE.facets["org_finding_policy_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": finding_policy.state.modified_date,
            "name": finding_policy.org_name,
            "uuid": finding_policy.id,
        },
        latest_facet=TABLE.facets["org_finding_policy_state"],
    )
    items = (initial_metadata, *historic_state)

    await operations.batch_write_item(items=items, table=TABLE)


async def update_org_finding_policy_state(
    *, org_name: str, finding_policy_id: str, state: OrgFindingPolicyState
) -> None:
    key_structure = TABLE.primary_key
    historic = historics.build_historic(
        attributes=dict(state._asdict()),
        historic_facet=TABLE.facets["org_finding_policy_historic_state"],
        key_structure=key_structure,
        key_values={
            "iso8601utc": state.modified_date,
            "name": org_name,
            "uuid": finding_policy_id,
        },
        latest_facet=TABLE.facets["org_finding_policy_state"],
    )

    await operations.batch_write_item(items=historic, table=TABLE)


async def create_group_metadata(*, group_metadata: GroupMetadata) -> None:
    key_structure = TABLE.primary_key
    facet = TABLE.facets["group_metadata"]
    metadata_key = keys.build_key(
        facet=facet, values={"name": group_metadata.name}
    )
    metadata = {
        key_structure.partition_key: metadata_key.partition_key,
        key_structure.sort_key: metadata_key.sort_key,
        **dict(group_metadata._asdict()),
    }
    condition_expression = Attr(key_structure.partition_key).not_exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=facet,
        item=metadata,
        table=TABLE,
    )


async def update_group_agent_token(
    *,
    group_name: str,
    agent_token: str,
) -> None:
    key_structure = TABLE.primary_key
    key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )
    item = {"agent_token": agent_token}
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=item,
        key=key,
        table=TABLE,
    )


async def get_agent_token(*, group_name: str) -> Optional[str]:
    primary_key = keys.build_key(
        facet=TABLE.facets["group_metadata"],
        values={"name": group_name},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["group_metadata"],),
        table=TABLE,
    )
    if results:
        return results[0]["agent_token"]

    return None
