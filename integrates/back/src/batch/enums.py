from enum import (
    Enum,
)


class JobStatus(str, Enum):
    SUBMITTED: str = "SUBMITTED"
    PENDING: str = "PENDING"
    RUNNABLE: str = "RUNNABLE"
    STARTING: str = "STARTING"
    RUNNING: str = "RUNNING"
    SUCCEEDED: str = "SUCCEEDED"
    FAILED: str = "FAILED"


class Product(str, Enum):
    INTEGRATES: str = "integrates"
    SKIMS: str = "skims"


class Action(str, Enum):
    REPORT = "report"
    REBASE = "rebase"
    MOVE_ROOT = "move_root"
    HANDLE_FINDING_POLICY = "handle_finding_policy"
    REFRESH_TOE_INPUTS = "refresh_toe_inputs"
    REFRESH_TOE_LINES = "refresh_toe_lines"
    REFRESH_TOE_PORTS = "refresh_toe_ports"
    CLONE_ROOTS = "clone_roots"
    REMOVE_ROOTS = "remove_roots"
    REMOVE_GROUP_RESOURCES = "remove_group_resources"
    EXECUTE_MACHINE = "execute-machine"
    UPDATE_ORGANIZATION_OVERVIEW = "update_organization_overview"
    UPDATE_ORGANIZATION_REPOSITORIES = "update_organization_repositories"
