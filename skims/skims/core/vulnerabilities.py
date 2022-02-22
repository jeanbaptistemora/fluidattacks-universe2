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

    for vulnerability in store.iterate():
        if vulnerability.integrates_metadata.verification:
            verification = vulnerability.integrates_metadata.verification.state
            if (
                verification
                == core_model.VulnerabilityVerificationStateEnum.REQUESTED
            ):
                reattacked_store.store(vulnerability)
    return reattacked_store


def get_vulnerability_justification(
    reattacked_store: EphemeralStore,
    store: EphemeralStore,
) -> str:
    line_content: str = ""
    today = get_iso_date()
    if reattacked_store:
        justification = f"Reattack request was executed in \
            {format_justification_date(today)}. "
        commits = []
        for reattacked_vuln in reattacked_store.iterate():
            commit_hash = reattacked_vuln.integrates_metadata.commit_hash
            for vuln in store.iterate():
                if (
                    vuln.where == reattacked_vuln.where
                    and vuln.what == reattacked_vuln.what
                ):
                    line_content = list(
                        filter(
                            lambda line: line.startswith(">"),
                            vuln.skims_metadata.snippet.splitlines(),
                        )
                    )[0]

            if commit_hash is not None:
                commits.append(
                    f"- Non-compliant code, Line {reattacked_vuln.where} \
                    with content: {line_content}"
                    if line_content is not None
                    else ""
                    if reattacked_vuln.where is not None
                    else commit_hash
                )

        str_commits = "\n- ".join(commits)

        justification += (
            f"Reported vulnerability is still open in commit: \
            {commit_hash} \n {str_commits}"
            if commits
            else ""
        )
    return justification
