from dynamodb.types import (
    Facet,
    PrimaryKey,
)

# Constants
RESERVED_WORDS: set[str] = {
    "#",
}


def _validate_key_words(*, key: str) -> None:
    for word in RESERVED_WORDS:
        if word in key:
            raise ValueError(
                f'Invalid key, got: {key} with invalid word: "{word}"'
            )


def _build_composite_key(*, template: str, values: dict[str, str]) -> str:
    template_parts = tuple(part for part in template.split("#"))
    key_parts = tuple(
        part if part.isupper() else values.get(part) for part in template_parts
    )

    return "#".join(part for part in key_parts if part)


def build_key(*, facet: Facet, values: dict[str, str]) -> PrimaryKey:
    for key in values:
        _validate_key_words(key=key)

    composite_pk: str = _build_composite_key(
        template=facet.pk_alias, values=values
    )
    composite_sk: str = _build_composite_key(
        template=facet.sk_alias, values=values
    )
    return PrimaryKey(
        partition_key=composite_pk,
        sort_key=composite_sk,
    )
