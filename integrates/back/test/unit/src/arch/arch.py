from arch_lint.dag import (
    DAG,
)
from typing import (
    FrozenSet,
    Tuple,
)

_dag: Tuple[FrozenSet[str], ...] = (
    frozenset({"cli"}),
    frozenset({"app"}),
    frozenset({"schedulers"}),
    frozenset({"api"}),
    frozenset({"batch_dispatch"}),
    frozenset({"companies"}),
    frozenset({"remove_stakeholder"}),
    frozenset({"unreliable_indicators"}),
    frozenset({"azure_repositories"}),
    frozenset({"billing"}),
    frozenset({"forces"}),
    frozenset({"reports"}),
    frozenset({"toe"}),
    frozenset({"groups"}),
    frozenset({"group_comments"}),
    frozenset({"events"}),
    frozenset({"vulnerability_files"}),
    frozenset({"findings"}),
    frozenset({"organizations_finding_policies"}),
    frozenset({"vulnerabilities"}),
    frozenset({"roots"}),
    frozenset({"notifications"}),
    frozenset({"event_comments"}),
    frozenset({"finding_comments"}),
    frozenset({"subscriptions"}),
    frozenset({"analytics"}),
    frozenset({"tags"}),
    frozenset({"decorators"}),
    frozenset({"organizations"}),
    frozenset({"mailer"}),
    frozenset({"stakeholders"}),
    frozenset({"group_access"}),
    frozenset({"authz"}),
    frozenset({"batch"}),
    frozenset({"newutils"}),
    frozenset({"sessions"}),
    frozenset({"dataloaders"}),
    frozenset({"db_model"}),
    frozenset({"dynamodb"}),
    frozenset({"s3"}),
    frozenset({"verify"}),
    frozenset({"settings"}),
    frozenset({"custom_exceptions"}),
    frozenset({"context"}),
    frozenset({"search"}),
    frozenset({"enrollment"}),
    frozenset({"telemetry"}),
    frozenset({"machine"}),
    frozenset({"sms"}),
    frozenset({"server"}),
)


def project_dag() -> DAG:
    result = DAG.new(_dag)
    if isinstance(result, Exception):
        raise result  # pylint: disable=raising-non-exception
    return result
