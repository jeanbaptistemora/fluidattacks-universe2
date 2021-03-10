# Standard
import json
from typing import Any, Dict

# Local
from dynamodb.types import Facet, Index, PrimaryKey, Table
from newutils.context import DB_MODEL_PATH


def load_facets(model: Dict[str, Any]) -> Dict[str, Facet]:
    return {
        facet['FacetName']: Facet(
            attrs=tuple(facet['NonKeyAttributes']),
            pk_alias=facet['KeyAttributeAlias']['PartitionKeyAlias'],
            sk_alias=facet['KeyAttributeAlias']['SortKeyAlias']
        )
        for facet in model['DataModel'][0]['TableFacets']
    }


def get_key(key_attrs: Dict[str, Any]) -> PrimaryKey:
    return PrimaryKey(
        partition_key=key_attrs['PartitionKey']['AttributeName'],
        sort_key=key_attrs['SortKey']['AttributeName']
    )


def load_indexes(model: Dict[str, Any]) -> Dict[str, Index]:
    data_model = model['DataModel'][0]

    return {
        index['IndexName']: Index(
            name=index['IndexName'],
            primary_key=get_key(index['KeyAttributes'])
        )
        for index in data_model['GlobalSecondaryIndexes']
    }


def load_table(model: Dict[str, Any]) -> Table:
    data_model = model['DataModel'][0]

    return Table(
        name=data_model['TableName'],
        primary_key=get_key(data_model['KeyAttributes']),
        facets=load_facets(model),
        indexes=load_indexes(model)
    )


with open(DB_MODEL_PATH, mode='r') as file:
    TABLE = load_table(json.loads(file.read()))
