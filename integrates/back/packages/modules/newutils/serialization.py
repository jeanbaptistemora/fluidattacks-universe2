# Third party libraries
import safe_pickle
from safe_pickle import (
    dump,
    load,
)

# Local libraries
from data_containers.toe_inputs import (
    GitRootToeInput,
)
from data_containers.toe_lines import (
    GitRootToeLines,
)


# Side effects
safe_pickle.register_namedtuple(GitRootToeInput)
safe_pickle.register_namedtuple(GitRootToeLines)

# Exported members
__all__ = ['dump', 'load']
