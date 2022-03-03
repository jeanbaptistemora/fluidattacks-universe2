from model import (
    core_model,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
)
from utils.time import (
    format_justification_date,
    get_iso_date,
)


def vulns_with_reattack_requested(
    store: EphemeralStore,
) -> EphemeralStore:
    vulnerability: core_model.Vulnerability
    reattacked_store: EphemeralStore = get_ephemeral_store()
    reattacked_flag: bool = False
    for vulnerability in store.iterate():
        if vulnerability.integrates_metadata.verification:
            verification = vulnerability.integrates_metadata.verification.state
            if (
                verification
                == core_model.VulnerabilityVerificationStateEnum.REQUESTED
            ):
                reattacked_flag = True
                reattacked_store.store(vulnerability)

    if reattacked_flag:
        return reattacked_store
    return None


def get_vulnerability_justification(
    reattacked_store: EphemeralStore,
    store: EphemeralStore,
) -> str:

    today = get_iso_date()
    commits = []
    commit_hash: str = ""
    line_content: str
    justification: str = ""

    if reattacked_store:
        for reattacked_vuln in reattacked_store.iterate():
            commit_hash = reattacked_vuln.integrates_metadata.commit_hash
            line_content = ""
            for vuln in store.iterate():
                if (
                    vuln.where == reattacked_vuln.where
                    and vuln.what == reattacked_vuln.what
                    and vuln.skims_metadata is not None
                ):
                    line_content = list(
                        filter(
                            lambda line: line.startswith(">"),
                            vuln.skims_metadata.snippet.splitlines(),
                        )
                    )[0]

            if commit_hash and line_content:
                commits.append(
                    f"- Non-compliant code, Line {reattacked_vuln.where} \
                    with content: {line_content}"
                    if reattacked_vuln.where is not None
                    else commit_hash
                )

        str_commits = "\n ".join(commits)

        justification = (
            f"Reported vulnerability is still open in commit: \
            {commit_hash} \n {str_commits}"
            if commits
            else ""
        )
        if justification != "":
            justification = (
                f"A reattack request was executed on \
            {format_justification_date(today).replace(' ', ' at ')}. "
                + justification
            )

    return justification
