from ctx import (
    CTX,
)
from model import (
    core_model,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
)
from typing import (
    List,
    Optional,
)
from utils.repositories import (
    get_repo_head_hash,
)
from utils.time import (
    format_justification_date,
    get_iso_date,
)


def vulns_with_reattack_requested(
    store: EphemeralStore,
) -> Optional[EphemeralStore]:
    vulnerability: core_model.Vulnerability
    reattacked_store: EphemeralStore = get_ephemeral_store()
    reattacked_flag: bool = False
    for vulnerability in store.iterate():
        integrates_metadata = vulnerability.integrates_metadata
        if integrates_metadata and integrates_metadata.verification:
            verification = integrates_metadata.verification.state
            if (
                verification
                == core_model.VulnerabilityVerificationStateEnum.REQUESTED
                and integrates_metadata.source
                == core_model.VulnerabilitySourceEnum.SKIMS
            ):
                reattacked_flag = True
                reattacked_store.store(vulnerability)

    if reattacked_flag:
        return reattacked_store
    return None


def get_vulnerability_justification(  # noqa: MC0001
    reattacked_store: Optional[EphemeralStore],
    store: EphemeralStore,
) -> List[str]:

    today = get_iso_date()
    open_vulns: List[str] = []
    closed_vulns: List[str] = []
    commit_hash: str = get_repo_head_hash(CTX.config.working_dir)
    line_content: str
    open_justification: str = ""
    closed_justification: str = ""

    if reattacked_store:
        for vuln in store.iterate():
            if vuln.state == core_model.VulnerabilityStateEnum.OPEN:
                line_content = ""
                for reattacked_vuln in reattacked_store.iterate():
                    if (
                        vuln.where == reattacked_vuln.where
                        and vuln.what == reattacked_vuln.what
                        and vuln.skims_metadata is not None
                        and vuln.kind == reattacked_vuln.kind
                    ):
                        line_content = list(
                            filter(
                                lambda line: line.startswith(">"),
                                vuln.skims_metadata.snippet.splitlines(),
                            )
                        )[0]

                if line_content:
                    if (
                        vuln.skims_metadata.technique
                        != core_model.TechniqueEnum.DAST
                    ):
                        open_vulns.append(
                            f"  - {vuln.what}:\n "
                            + f"    Non-compliant code: {line_content}"
                        )
                    else:
                        open_vulns.append(f"  - {vuln.what} ")
            else:
                for reattacked_vuln in reattacked_store.iterate():
                    if (
                        vuln.where == reattacked_vuln.where
                        and vuln.what == reattacked_vuln.what
                        and vuln.kind == reattacked_vuln.kind
                    ):
                        closed_vulns.append(f"  - {vuln.what}")

        str_open_vulns = "\n ".join(open_vulns) if open_vulns else ""

        open_justification = (
            "Reported vulnerabilities are still open in commit "
            + f"{commit_hash}: \n {str_open_vulns}"
            if open_vulns
            else ""
        )
        if open_justification:
            open_justification = (
                "A reattack request was executed on "
                + f"{format_justification_date(today).replace(' ', ' at ')}.\n"
                + open_justification
            )

        str_closed_vulns = "\n".join(closed_vulns)

        closed_justification = (
            "Reattack request was executed on "
            + f"{format_justification_date(today).replace(' ', ' at ')}. \n"
            + "Reported vulnerabilities were solved "
            + f"in commit {commit_hash}: \n"
            + f"{str_closed_vulns} \n"
            if closed_vulns
            else ""
        )

    justification = [open_justification, closed_justification]
    justification = [item for item in justification if item]
    return justification
