from model import (
    core_model,
)
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
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
