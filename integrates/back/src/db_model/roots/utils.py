from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
    RootType,
)
from db_model.roots.types import (
    GitRoot,
    GitRootCloning,
    GitRootState,
    IPRoot,
    IPRootState,
    Root,
    RootUnreliableIndicators,
    URLRoot,
    URLRootState,
)
from dynamodb.types import (
    Item,
)


def format_unreliable_indicators(
    unreliable_indicators: Item,
) -> RootUnreliableIndicators:
    return RootUnreliableIndicators(
        unreliable_last_status_update=unreliable_indicators[
            "unreliable_last_status_update"
        ]
    )


def format_git_state(state: Item) -> GitRootState:
    return GitRootState(
        branch=state["branch"],
        environment_urls=state["environment_urls"],
        environment=state["environment"],
        git_environment_urls=[],
        gitignore=state["gitignore"],
        includes_health_check=state["includes_health_check"],
        modified_by=state["modified_by"],
        modified_date=state["modified_date"],
        nickname=state["nickname"],
        other=state.get("other"),
        reason=state.get("reason"),
        status=RootStatus[state["status"]],
        url=state["url"],
        download_url=None,
        secrets=[],
        upload_url=None,
        use_vpn=state.get("use_vpn", False),
    )


def format_ip_state(state: Item) -> IPRootState:
    return IPRootState(
        address=state["address"],
        modified_by=state["modified_by"],
        modified_date=state["modified_date"],
        nickname=state["nickname"],
        other=state.get("other"),
        port=state["port"],
        reason=state.get("reason"),
        status=RootStatus[state["status"]],
    )


def format_url_state(state: Item) -> URLRootState:
    return URLRootState(
        host=state["host"],
        modified_by=state["modified_by"],
        modified_date=state["modified_date"],
        nickname=state["nickname"],
        other=state.get("other"),
        path=state["path"],
        port=state["port"],
        protocol=state["protocol"],
        query=state.get("query"),
        reason=state.get("reason"),
        status=RootStatus[state["status"]],
    )


def format_cloning(cloning: Item) -> GitRootCloning:
    return GitRootCloning(
        modified_date=cloning["modified_date"],
        reason=cloning["reason"],
        status=GitCloningStatus(cloning["status"]),
        commit=cloning.get("commit"),
        commit_date=cloning.get("commit_date"),
    )


def format_root(item: Item) -> Root:
    root_id = item["pk"].split("#")[1]
    group_name = item["sk"].split("#")[1]
    organization_name = item["pk_2"].split("#")[1]
    unreliable_indicators = (
        format_unreliable_indicators(item["unreliable_indicators"])
        if "unreliable_indicators" in item
        else RootUnreliableIndicators()
    )

    if item["type"] == "Git":
        return GitRoot(
            cloning=format_cloning(item["cloning"]),
            group_name=group_name,
            id=root_id,
            organization_name=organization_name,
            state=format_git_state(item["state"]),
            type=RootType.GIT,
            unreliable_indicators=unreliable_indicators,
        )

    if item["type"] == "IP":
        return IPRoot(
            group_name=group_name,
            id=root_id,
            organization_name=organization_name,
            state=format_ip_state(item["state"]),
            type=RootType.IP,
            unreliable_indicators=unreliable_indicators,
        )

    return URLRoot(
        group_name=group_name,
        id=root_id,
        organization_name=organization_name,
        state=format_url_state(item["state"]),
        type=RootType.URL,
        unreliable_indicators=unreliable_indicators,
    )
