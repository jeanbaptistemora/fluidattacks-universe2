# Standard library
from datetime import datetime

# Third party libraries
from graphene import DateTime, List, ObjectType, String

# Local libraries
from backend.util import get_current_time_minus_delta
from backend.dal import break_build as break_build_dal

# pylint: disable=super-init-not-called

# Constants
DYNAMO_DB_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'


class BreakBuildExecution(ObjectType):
    """ GraphQL Entity for a Break Build Execution """
    project_name = String()
    identifier = String()
    date = DateTime()

    def __init__(self, *,
                 subscription: str,
                 execution_id: str,
                 date: datetime,
                 **_):
        self.project_name: str = subscription
        self.identifier: str = execution_id
        self.date: datetime = datetime.strptime(date, DYNAMO_DB_DATE_FORMAT)

    def __str__(self):
        return f'BreakBuildExecution({self.project_name}, {self.identifier})'

    def resolve_project_name(self, info):
        """ Resolve project_name """
        del info
        return self.project_name

    def resolve_identifier(self, info):
        """ Resolve identifier """
        del info
        return self.identifier

    def resolve_date(self, info):
        """ Resolve date """
        del info
        return self.date


class BreakBuildExecutions(ObjectType):
    """ GraphQL Entity for the Break Build Executions """
    project_name = String()
    from_date = DateTime()
    to_date = DateTime()
    executions = List(BreakBuildExecution)

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
        return f'BreakBuildExecutions({self.project_name})'

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

        executions_iterator = break_build_dal.yield_executions(
            project_name=self.project_name,
            from_date=self.from_date,
            to_date=self.to_date)

        return [
            BreakBuildExecution(**execution)
            for execution in executions_iterator
        ]
