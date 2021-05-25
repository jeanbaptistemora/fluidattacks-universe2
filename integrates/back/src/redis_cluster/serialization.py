import safe_pickle
from safe_pickle import (
    dump,
    load,
)


from data_containers.toe_inputs import GitRootToeInput
from data_containers.toe_lines import GitRootToeLines
from db_model.findings.enums import FindingStateStatus
from db_model.findings.types import FindingState


# Side effects
safe_pickle.register_enum(FindingStateStatus)
safe_pickle.register_namedtuple(FindingState)
safe_pickle.register_namedtuple(GitRootToeInput)
safe_pickle.register_namedtuple(GitRootToeLines)

# Exported members
__all__ = ["dump", "load"]
