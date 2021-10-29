from datetime import (
    datetime as dt,
)
from dateutil.relativedelta import (  # type: ignore
    relativedelta,
)
from toolbox import (
    api,
)
from toolbox.api.integrates import (
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
)

BASE_URL: str = "https://app.fluidattacks.com"


def get_subs_unverified_findings(group: str = "all") -> Response:

    project_info_query: str = """
        name
        findings(filters: {verified: false}) {
            id
            vulnerabilitiesToReattack {
                id
                historicVerification {
                    status, date
                }
            }
        }
    """

    if group == "all":
        query = f"""
            query {{
                me {{
                    organizations {{
                        groups {{
                            {project_info_query}
                        }}
                    }}
                }}
            }}
        """
    else:
        query = f"""
            query{{
                group(groupName: "{group}") {{
                    {project_info_query}
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
    projects_info = response.data if response.status_code == 200 else {}

    if group != "all":
        projects_info = {
            "me": {"organizations": [{"groups": [projects_info.get("group")]}]}
        }
    projects_info = [
        group
        for org in projects_info.get("me", {}).get("organizations", {})
        for group in org.get("groups", [])
    ]

    # claning empty findigs
    projects_info = list(
        filter(
            lambda info: info.get("findings")
            and [
                finding.get("vulnerabilitiesToReattack")
                for finding in info.get("findings", [{}])
            ],
            projects_info,
        )
    )

    # Filter vulnerabilities and order by date
    for project_info in projects_info:
        for finding in project_info["findings"]:
            # Order vulnerabilities by date
            finding["vulnerabilities"] = list(
                sorted(
                    finding["vulnerabilitiesToReattack"],
                    key=lambda x: x["historicVerification"][-1]["date"]
                    if x["historicVerification"]
                    else "2000-01-01 00:00:00",
                )
            )

        project_info["findings"] = list(
            filter(
                lambda finding: finding["vulnerabilities"],
                project_info["findings"],
            )
        )

    total_findings = 0
    total_vulnerabilities = 0
    oldest_finding = {"group": "", "date_dif": relativedelta()}
    for project_info in projects_info:
        for finding in project_info["findings"]:
            oldest_vulnerability = finding["vulnerabilities"][0]
            oldest_vuln_dif = relativedelta(
                dt.now(),
                dt.strptime(
                    oldest_vulnerability["historicVerification"][-1]["date"]
                    if oldest_vulnerability["historicVerification"]
                    else "2000-01-01 00:00:00",
                    graphql_date_format,
                ),
            )
            finding["vulnerability_counter"] = len(finding["vulnerabilities"])
            finding["oldest_vuln_dif"] = oldest_vuln_dif
            finding["url"] = get_url(project_info["name"], finding["id"])

            total_vulnerabilities += finding["vulnerability_counter"]
            if (
                oldest_finding["date_dif"].days
                < finding["oldest_vuln_dif"].days
            ):

                oldest_finding = {
                    "group": project_info["name"],
                    "date_dif": finding["oldest_vuln_dif"],
                }

        total_findings += len(project_info["findings"])

    # cleaning findings without vulnerabilities
    for project_info in projects_info:
        project_info["findings"] = list(
            filter(
                lambda finding: finding["vulnerabilities"],
                project_info["findings"],
            )
        )
    # clean trash
    projects_info = list(
        filter(lambda project_info: project_info["findings"], projects_info)
    )

    summary_info = {
        "total_findings": total_findings,
        "total_vulnerabilities": total_vulnerabilities,
        "oldest_finding": oldest_finding,
    }

    return {"projects_info": projects_info, "summary_info": summary_info}


@shield()
def main(group: str = "all") -> None:
    """
    Print all non-verified findings and their exploits
    """
    to_reattack_search = to_reattack(group)

    projects_info = to_reattack_search["projects_info"]
    summary_info = to_reattack_search["summary_info"]

    for project_info in projects_info:
        if project_info["findings"]:
            # Head
            print(project_info["name"])
            # Body
            for finding in project_info["findings"]:
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
