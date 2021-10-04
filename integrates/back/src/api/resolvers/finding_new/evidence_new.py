from db_model.findings.types import (
    Finding,
    FindingEvidence,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    Dict,
    Optional,
)


def _format_evidence(
    finding: Finding, evidence: Optional[FindingEvidence]
) -> Dict[str, str]:
    # pylint: disable=unsubscriptable-object
    return (
        {
            "description": "",
            "url": "",
        }
        if evidence is None
        else {
            "date": datetime_utils.get_as_str(
                findings_domain.get_updated_evidence_date_new(
                    finding, evidence
                )
            ),
            "description": evidence.description,
            "url": evidence.url,
        }
    )


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, Dict[str, str]]:
    return {
        "animation": _format_evidence(parent, parent.evidences.animation),
        "evidence1": _format_evidence(parent, parent.evidences.evidence1),
        "evidence2": _format_evidence(parent, parent.evidences.evidence2),
        "evidence3": _format_evidence(parent, parent.evidences.evidence3),
        "evidence4": _format_evidence(parent, parent.evidences.evidence4),
        "evidence5": _format_evidence(parent, parent.evidences.evidence5),
        "exploitation": _format_evidence(
            parent, parent.evidences.exploitation
        ),
    }
