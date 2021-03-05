# Standard library
from typing import (
    Dict,
    Optional,
    Set
)

# Third party
from boto3.dynamodb.conditions import Key

# Local
from backend.dal.helpers import dynamodb
from backend.model.dynamo import versioned
from backend.model.dynamo.types import (
    Entity,
    PrimaryKey,
    RootHistoricCloning,
    RootHistoricState,
    RootItem,
    RootMetadata
)


# Constants
RESERVED_WORDS: Set[str] = {
    '#',
    '/',
}

ENTITIES: Dict[str, Entity] = dict(
    ROOT=Entity(
        primary_key=PrimaryKey(
            partition_key='GROUP#',
            sort_key='ROOT#',
        ),
    ),
)

TABLE_NAME = 'integrates_vms'


def validate_pkey_not_empty(*, key: str) -> None:
    if not key:
        raise ValueError(f'Partition key cannot be empty')


def validate_entity(*, entity: str) -> None:
    if entity not in ENTITIES:
        raise ValueError(f'Invalid entity: {entity}')


def validate_key_type(*, key: str) -> None:
    if not isinstance(key, str):
        raise TypeError(f'Expected str, got: {type(key)}')


def validate_key_words(*, key: str) -> None:
    for word in RESERVED_WORDS:
        if word in key:
            raise ValueError(
                f'Invalid key, got: {key} with invalid word: "{word}"'
            )


def build_key(*, entity: str, partition_key: str, sort_key: str) -> PrimaryKey:
    validate_entity(entity=entity)
    validate_pkey_not_empty(key=partition_key)
    for key in {partition_key, sort_key}:
        validate_key_type(key=key)
        validate_key_words(key=key)

    prefix = ENTITIES[entity].primary_key
    composite_pkey: str = f'{prefix.partition_key}{partition_key}'
    composite_skey: str = (
        f'{prefix.sort_key}{sort_key}'
        if sort_key
        else prefix.sort_key
    )

    # >>> build_key(entity='ROOT', partition_key='group-1', sort_key='root-1')
    # PrimaryKey(partition_key='GROUP#group-1', sort_key='ROOT#root-1')
    # >>> build_key(entity='ROOT', partition_key='group-1', sort_key='')
    # PrimaryKey(partition_key='GROUP#group-1', sort_key='')
    return PrimaryKey(
        partition_key=composite_pkey,
        sort_key=composite_skey,
    )


async def get_root(
    *,
    group_name: str,
    url: str,
    branch: str
) -> Optional[RootItem]:
    primary_key = build_key(
        entity='ROOT',
        partition_key=group_name,
        sort_key=''.join([url, branch])
    )

    results = await dynamodb.async_query(
        TABLE_NAME,
        {
            'IndexName': 'inverted_index',
            'KeyConditionExpression': (
                Key('sk').eq(primary_key.partition_key) &
                Key('pk').begins_with(primary_key.sort_key)
            )
        }
    )

    if results:
        historic_cloning = versioned.get_historic(
            primary_key=primary_key,
            historic_prefix='HIST',
            raw_items=results
        )
        historic_state = versioned.get_historic(
            primary_key=primary_key,
            historic_prefix='CLON',
            raw_items=results
        )
        metadata = versioned.get_metadata(
            primary_key=primary_key,
            raw_items=results
        )

        return RootItem(
            historic_cloning=tuple(
                RootHistoricCloning(
                    modified_date=item['modified_date'],
                    reason=item['reason'],
                    status=item['status']
                )
                for item in historic_cloning
            ),
            historic_state=tuple(
                RootHistoricState(
                    environment_urls=item['environment_urls'],
                    environment=item['environment'],
                    gitignore=item['gitignore'],
                    includes_health_check=item['includes_health_check'],
                    modified_by=item['modified_by'],
                    modified_date=item['modified_date'],
                    status=item['status']
                )
                for item in historic_state
            ),
            metadata=RootMetadata(
                branch=metadata['branch'],
                type=metadata['type'],
                url=metadata['url']
            )
        )

    return None
