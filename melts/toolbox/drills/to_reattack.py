from datetime import (
    datetime as dt,
)
from dateutil.relativedelta import (
    relativedelta,
)
from toolbox import (
    api,
)
from toolbox.api.integrates import (
    get_paginated_fields,
    Response,
)
from toolbox.constants import (
    API_TOKEN,
)
from toolbox.utils.function import (
    shield,
)
from typing import (
    Any,
    Dict,
    List,
)

BASE_URL: str = "https://app.fluidattacks.com"


def get_subs_unverified_findings(group: str = "all") -> Response:

    group_info_query: str = """
        name
        findings(filters: {verified: false}) {
            id
        }
    """

    if group == "all":
        query = f"""
            query {{
                me {{
                    organizations {{
                        groups {{
                            {group_info_query}
                        }}
                    }}
                }}
            }}
        """
    else:
        query = f"""
            query{{
                group(groupName: "{group}") {{
                    {group_info_query}
                }}
            }}
        """
    return api.integrates.request(API_TOKEN, query)


def get_url(subs_name: str, finding_id: str) -> str:
    """Return a string with an url associated to a subs finding"""
    return f"{BASE_URL}/groups/{subs_name}/vulns/{finding_id}"


def to_reattack(group: str = "all") -> Dict[str, Any]:
    """
    Return a string with non-verified findings from a subs.
    It includes integrates url and exploits paths in case they exist

    param: group: Name of the group to check
    """
    graphql_date_format = "%Y-%m-%d %H:%M:%S"

    response = get_subs_unverified_findings(group)
    groups_data = response.data if response.status_code == 200 else {}

    if group != "all":
        groups_data = {
            "me": {"organizations": [{"groups": [groups_data.get("group")]}]}
        }
    groups_info: List[Dict[str, Any]] = [
        dict(group_data)
        for org in groups_data.get("me", {}).get("organizations", {})
        for group_data in org.get("groups", [])
    ]

    vulns_to_reattack_query: str = """
        query MeltsGetVulnerabilitiesToReattack(
            $after: String
            $finding_id: String!
            $first: Int
        ) {
            finding(identifier: $finding_id) {
                id
                vulnerabilitiesToReattackConnection(
                    after: $after,
                    first: $first,
                ) {
                    edges {
                        node {
                            id
                            lastVerificationDate
                        }
                    }
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                }
            }
        }
    """

    # Filling vulnerability info
    for group_data in groups_info:
        for finding in group_data["findings"]:
            finding["vulnerabilitiesToReattack"] = get_paginated_fields(
                api_token=API_TOKEN,
                paginated_field="vulnerabilitiesToReattackConnection",
                parent_field="finding",
                params=dict(finding_id=finding["id"]),
                query=vulns_to_reattack_query,
            )

    # cleaning empty findigs
    groups_info = list(
        filter(
            lambda info: info.get("findings")
            and [
                finding.get("vulnerabilitiesToReattack")
                for finding in info.get("findings", [{}])
            ],
            groups_info,
        )
    )

    # Filter vulnerabilities and order by date
    for group_info in groups_info:
        for finding in group_info["findings"]:
            # Order vulnerabilities by date
            finding["vulnerabilities"] = list(
                sorted(
                    finding["vulnerabilitiesToReattack"],
                    key=lambda x: x["lastVerificationDate"]
                    if x["lastVerificationDate"]
                    else "2000-01-01 00:00:00",
                )
            )

        group_info["findings"] = list(
            filter(
                lambda finding: finding["vulnerabilities"],
                group_info["findings"],
            )
        )

    total_findings = 0
    total_vulnerabilities = 0
    oldest_finding = {"group": "", "date_dif": relativedelta()}
    for group_info in groups_info:
        for finding in group_info["findings"]:
            oldest_vulnerability = finding["vulnerabilities"][0]
            oldest_vuln_dif = relativedelta(
                dt.now(),
                dt.strptime(
                    oldest_vulnerability["lastVerificationDate"]
                    if oldest_vulnerability["lastVerificationDate"]
                    else "2000-01-01 00:00:00",
                    graphql_date_format,
                ),
            )
            finding["vulnerability_counter"] = len(finding["vulnerabilities"])
            finding["oldest_vuln_dif"] = oldest_vuln_dif
            finding["url"] = get_url(group_info["name"], finding["id"])

            total_vulnerabilities += finding["vulnerability_counter"]
            if (
                oldest_finding["date_dif"].days  # type: ignore
                < finding["oldest_vuln_dif"].days
            ):

                oldest_finding = {
                    "group": group_info["name"],
                    "date_dif": finding["oldest_vuln_dif"],
                }

        total_findings += len(group_info["findings"])

    # cleaning findings without vulnerabilities
    for group_info in groups_info:
        group_info["findings"] = list(
            filter(
                lambda finding: finding["vulnerabilities"],
                group_info["findings"],
            )
        )
    # clean trash
    groups_info = list(
        filter(lambda project_info: project_info["findings"], groups_info)
    )

    summary_info = {
        "total_findings": total_findings,
        "total_vulnerabilities": total_vulnerabilities,
        "oldest_finding": oldest_finding,
    }

    return {"groups_info": groups_info, "summary_info": summary_info}


@shield()
def main(group: str = "all") -> None:
    """
    Print all non-verified findings and their exploits
    """
    to_reattack_search = to_reattack(group)

    groups_info = to_reattack_search["groups_info"]
    summary_info = to_reattack_search["summary_info"]

    for group_info in groups_info:
        if group_info["findings"]:
            # Head
            print(group_info["name"])
            # Body
            for finding in group_info["findings"]:
                print(
                    "  url:               "
                    f'{finding["url"]}\n'
                    "  requested (days):  "
                    f'{finding["oldest_vuln_dif"].days}\n'
                    "  vulns to verify:   "
                    f'{finding["vulnerability_counter"]}'
                )
                print()
            print()

    # summary
    summary = (
        f"TO-DO: Findings: {summary_info['total_findings']}; "
        f"Vulns: {summary_info['total_vulnerabilities']}; "
        "Days since oldest request: "
        f"{summary_info['oldest_finding']['date_dif'].days}; "
        f"Group oldest finding: {summary_info['oldest_finding']['group']};"
    )

    print(summary)
