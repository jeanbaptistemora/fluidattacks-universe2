# disable MyPy due to error alert for outer __init__ attributes,
# which are all required by Graphene ObjectType
#  type: ignore

# Standard library
from datetime import datetime

# Third party libraries
from graphene import DateTime, Int, Field, List, ObjectType, String

# Local libraries
from backend.util import get_current_time_minus_delta
from backend.dal import forces as forces_dal

# pylint: disable=super-init-not-called
# pylint: disable=too-many-instance-attributes

# Constants
DYNAMO_DB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class ExploitResult(ObjectType):
    """ GraphQL Entity to represent the result of an exploit """
    kind = String()
    where = String()
    who = String()

    def __init__(self, *,
                 kind: str,
                 who: str,
                 where: str,
                 **_):
        self.kind: str = kind
        self.where: str = where
        self.who: str = who


class Vulnerabilities(ObjectType):
    """ GraphQL Entity for the vulnerabilities found in the logs """
    exploits = List(ExploitResult)
    mocked_exploits = List(ExploitResult)
    accepted_exploits = List(ExploitResult)
    num_of_vulnerabilities_in_exploits = Int()
    num_of_vulnerabilities_in_mocked_exploits = Int()
    num_of_vulnerabilities_in_accepted_exploits = Int()

    def __init__(self, *,
                 exploits: list,
                 mocked_exploits: list,
                 accepted_exploits: list,
                 vulnerability_count_exploits: int,
                 vulnerability_count_mocked_exploits: int,
                 vulnerability_count_accepted_exploits: int,
                 **_):
        self.exploits: list = \
            [ExploitResult(**args) for args in exploits]
        self.mocked_exploits: list = \
            [ExploitResult(**args) for args in mocked_exploits]
        self.accepted_exploits: list = \
            [ExploitResult(**args) for args in accepted_exploits]

        self.num_of_vulnerabilities_in_exploits: int = \
            vulnerability_count_exploits
        self.num_of_vulnerabilities_in_mocked_exploits: int = \
            vulnerability_count_mocked_exploits
        self.num_of_vulnerabilities_in_accepted_exploits: int = \
            vulnerability_count_accepted_exploits


class ForcesExecution(ObjectType):
    """ GraphQL Entity for a Forces Execution """
    project_name = String()
    identifier = String()
    date = DateTime()
    exit_code = String()
    git_branch = String()
    git_commit = String()
    git_origin = String()
    git_repo = String()
    kind = String()
    log = String()
    strictness = String()
    vulnerabilities = Field(Vulnerabilities)

    def __init__(self, *,
                 subscription: str,
                 execution_id: str,
                 date: datetime,
                 exit_code: str,
                 git_branch: str,
                 git_commit: str,
                 git_origin: str,
                 git_repo: str,
                 kind: str,
                 log: str,
                 strictness: str,
                 vulnerabilities: dict,
                 **_):
        self.project_name: str = subscription
        self.identifier: str = execution_id
        self.date: datetime = datetime.strptime(date, DYNAMO_DB_DATE_FORMAT)
        self.exit_code: str = exit_code
        self.git_branch: str = git_branch
        self.git_commit: str = git_commit
        self.git_origin: str = git_origin
        self.git_repo: str = git_repo
        self.kind: str = kind
        self.log: str = log
        self.strictness: str = strictness
        self.vulnerabilities: Vulnerabilities = \
            Vulnerabilities(**vulnerabilities)

    def __str__(self):
        return f'ForcesExecution({self.project_name}, {self.identifier})'


class ForcesExecutions(ObjectType):
    """ GraphQL Entity for the Forces Executions """
    project_name = String()
    from_date = DateTime()
    to_date = DateTime()
    executions = List(ForcesExecution)

    def __init__(self,
                 project_name: str,
                 from_date: datetime = None,
                 to_date: datetime = None):
        self.project_name: str = project_name
        self.from_date: datetime = \
            from_date or get_current_time_minus_delta(weeks=1)
        self.to_date: datetime = \
            to_date or datetime.utcnow()

    def __str__(self):
        return f'ForcesExecutions({self.project_name})'

    def resolve_project_name(self, info):
        """ Resolve project_name """
        del info
        return self.project_name

    def resolve_from_date(self, info):
        """ Resolve from_date """
        del info
        return self.from_date

    def resolve_to_date(self, info):
        """ Resolve to_date """
        del info
        return self.to_date

    def resolve_executions(self, info):
        """ Resolve executions """
        del info

        executions_iterator = forces_dal.yield_executions(
            project_name=self.project_name,
            from_date=self.from_date,
            to_date=self.to_date)

        return [
            ForcesExecution(**execution)
            for execution in executions_iterator
        ]
