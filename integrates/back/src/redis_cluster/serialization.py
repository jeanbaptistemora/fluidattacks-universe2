from db_model.enums import (
    Source,
)
from db_model.findings.enums import (
    FindingSorts,
    FindingStateJustification,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from db_model.findings.types import (
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerification,
)
from db_model.services_toe_lines.types import (
    ServicesToeLines,
)
from db_model.toe_inputs.types import (
    ToeInput,
)
import safe_pickle
from safe_pickle import (
    _deserialize,
    dump,
    dump_raw,
    load,
    serialize,
    Serialized,
)
from typing import (
    Any,
    List,
    Set,
)


def set_dump(instance: List[Any]) -> Serialized:
    return serialize(instance, *map(dump_raw, instance))


def set_load(*args: Serialized) -> Set[Any]:
    return set(map(_deserialize, args))


# Side effects
safe_pickle.register(set, set_dump, set_load)
safe_pickle.register_enum(FindingSorts)
safe_pickle.register_enum(FindingStateJustification)
safe_pickle.register_enum(FindingStateStatus)
safe_pickle.register_enum(FindingStatus)
safe_pickle.register_enum(FindingVerificationStatus)
safe_pickle.register_enum(Source)
safe_pickle.register_namedtuple(Finding)
safe_pickle.register_namedtuple(Finding20Severity)
safe_pickle.register_namedtuple(Finding31Severity)
safe_pickle.register_namedtuple(FindingEvidence)
safe_pickle.register_namedtuple(FindingEvidences)
safe_pickle.register_namedtuple(FindingState)
safe_pickle.register_namedtuple(FindingUnreliableIndicators)
safe_pickle.register_namedtuple(FindingTreatmentSummary)
safe_pickle.register_namedtuple(FindingVerification)
safe_pickle.register_namedtuple(ToeInput)
safe_pickle.register_namedtuple(ServicesToeLines)

# Exported members
__all__ = ["dump", "load"]
