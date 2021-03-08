# Standard
import json
from typing import Any, Dict, Tuple

# Local
from dynamodb.types import Facet
from newutils.context import DB_MODEL_PATH


def get_prefix(alias: str) -> str:
    return alias.split('#')[0]


def load_facets(model: Dict[str, Any]) -> Tuple[Facet, ...]:
    return tuple(
        Facet(
            attrs=tuple(facet['NonKeyAttributes']),
            name=facet['FacetName'],
            pk_prefix=get_prefix(
                facet['KeyAttributeAlias']['PartitionKeyAlias']
            ),
            sk_prefix=get_prefix(
                facet['KeyAttributeAlias']['SortKeyAlias']
            )
        )
        for facet in model['DataModel'][0]['TableFacets']
    )


with open(DB_MODEL_PATH, mode='r') as file:
    MODEL = json.loads(file.read())
    FACETS = load_facets(MODEL)
