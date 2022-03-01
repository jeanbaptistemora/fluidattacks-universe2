from enum import (
    Enum,
)


class JobStatus(Enum):
    SUBMITTED: str = "SUBMITTED"
    PENDING: str = "PENDING"
    RUNNABLE: str = "RUNNABLE"
    STARTING: str = "STARTING"
    RUNNING: str = "RUNNING"
    SUCCEEDED: str = "SUCCEEDED"
    FAILED: str = "FAILED"


class Product(Enum):
    INTEGRATES: str = "integrates"
    SKIMS: str = "skims"


class Action(Enum):
    REPORT = "report"
    MOVE_ROOT = "move_root"
    HANDLE_FINDING_POLICY = "handle_finding_policy"
    HANDLE_VIRUS_SCAN = "handle_virus_scan"
    REFRESH_TOE_INPUTS = "refresh_toe_inputs"
    REFRESH_TOE_LINES = "refresh_toe_lines"
    CLONE_ROOTS = "clone_roots"
    REMOVE_GROUP_RESOURCES = "remove_group_resources"
    EXECUTE_MACHINE = "execute-machine"
