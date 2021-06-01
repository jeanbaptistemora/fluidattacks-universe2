from db_model.findings.types import (
    Finding,
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
)


def resolve(
    parent: Finding, _info: GraphQLResolveInfo, **_kwargs: None
) -> Dict[str, Dict[str, str]]:
    return {
        name: {
            "description": "",
            "url": "",
        }
        if evidence is None
        else {
            "date": datetime_utils.get_as_str(
                findings_domain.get_updated_evidence_date_new(parent, evidence)
            ),
            "description": evidence.description,
            "url": evidence.url,
        }
        for name, evidence in zip(parent.evidences._fields, parent.evidences)
    }
