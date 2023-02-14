from datetime import (
    datetime,
)
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
        unreliable_code_languages=unreliable_indicators.get(
            "unreliable_code_languages", []
        ),
        unreliable_last_status_update=datetime.fromisoformat(
            unreliable_indicators["unreliable_last_status_update"]
        )
        if unreliable_indicators.get("unreliable_last_status_update")
        else None,
    )


def format_git_state(state: Item) -> GitRootState:
    return GitRootState(
        branch=state["branch"],
        credential_id=state.get("credential_id"),
        environment_urls=state["environment_urls"],
        environment=state["environment"],
        gitignore=state["gitignore"],
        includes_health_check=state["includes_health_check"],
        modified_by=state["modified_by"],
        modified_date=datetime.fromisoformat(state["modified_date"]),
        nickname=state["nickname"],
        other=state.get("other"),
        reason=state.get("reason"),
        status=RootStatus[state["status"]],
        url=state["url"],
        use_vpn=state.get("use_vpn", False),
    )


def format_ip_state(state: Item) -> IPRootState:
    return IPRootState(
        address=state["address"],
        modified_by=state["modified_by"],
        modified_date=datetime.fromisoformat(state["modified_date"]),
        nickname=state["nickname"],
        other=state.get("other"),
        reason=state.get("reason"),
        status=RootStatus[state["status"]],
    )


def format_url_state(state: Item) -> URLRootState:
    return URLRootState(
        host=state["host"],
        modified_by=state["modified_by"],
        modified_date=datetime.fromisoformat(state["modified_date"]),
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
        modified_date=datetime.fromisoformat(cloning["modified_date"]),
        reason=cloning["reason"],
        status=GitCloningStatus(cloning["status"]),
        commit=cloning.get("commit"),
        commit_date=datetime.fromisoformat(cloning["commit_date"])
        if cloning.get("commit_date")
        else None,
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
            created_by=item.get("created_by", "-"),
            created_date=datetime.fromisoformat(item["created_date"]),
            group_name=group_name,
            id=root_id,
            organization_name=organization_name,
            state=format_git_state(item["state"]),
            type=RootType.GIT,
            unreliable_indicators=unreliable_indicators,
        )

    if item["type"] == "IP":
        return IPRoot(
            created_by=item["created_by"],
            created_date=datetime.fromisoformat(item["created_date"]),
            group_name=group_name,
            id=root_id,
            organization_name=organization_name,
            state=format_ip_state(item["state"]),
            type=RootType.IP,
            unreliable_indicators=unreliable_indicators,
        )

    return URLRoot(
        created_by=item["created_by"],
        created_date=datetime.fromisoformat(item["created_date"]),
        group_name=group_name,
        id=root_id,
        organization_name=organization_name,
        state=format_url_state(item["state"]),
        type=RootType.URL,
        unreliable_indicators=unreliable_indicators,
    )
