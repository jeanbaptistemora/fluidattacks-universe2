from aioextensions import (
    collect,
)
import collections
from custom_types import (
    Finding as FindingType,
    Group as GroupType,
)
import re
from typing import (
    Any,
    Dict,
    List,
    Tuple,
)


def camel_case_list_dict(elements: List[Dict]) -> List[Dict]:
    """Convert a the keys of a list of dicts to camelcase."""
    return [
        {snakecase_to_camelcase(k): element[k] for k in element}
        for element in elements
    ]


def camelcase_to_snakecase(str_value: str) -> str:
    """Convert a camelcase string to snackecase."""
    my_str = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", str_value)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", my_str).lower()


async def get_filtered_elements(
    elements: List[FindingType], filters: Dict[str, Any]
) -> List[GroupType]:
    """Return filtered findings accorging to filters."""

    async def satisfies_filter(element: FindingType) -> bool:
        hits = 0
        for attribute, value in filters.items():
            result = element.get(camelcase_to_snakecase(attribute))
            if str(result) == str(value):
                hits += 1
        return hits == len(filters)

    conditions = await collect(map(satisfies_filter, elements))
    return [
        element
        for element, condition in zip(elements, conditions)
        if condition
    ]


def list_to_dict(
    keys: List[object], values: List[object]
) -> Dict[object, object]:
    """ Merge two lists into a {key: value} dictionary """
    dct: Dict[object, object] = collections.OrderedDict()
    index = 0

    if len(keys) < len(values):
        diff = len(values) - len(keys)
        for i in range(diff):
            del i
            keys.append("")
    elif len(keys) > len(values):
        diff = len(keys) - len(values)
        for i in range(diff):
            del i
            values.append("")
    else:
        # Each key has a value associated, so there's no need to empty-fill
        pass

    for item in values:
        if keys[index] == "":
            dct[index] = item
        else:
            dct[keys[index]] = item
        index += 1
    return dct


def snakecase_to_camelcase(str_value: str) -> str:
    """Convert a snakecase string to camelcase."""
    return re.sub("_.", lambda x: x.group()[1].upper(), str_value)


def replace_all(text: str, dic: Dict[str, str]) -> str:
    for i, j in list(dic.items()):
        text = text.replace(i, j)
    return text


# Standardization helper utils


def clean_up_kwargs(
    kwargs: Dict, keys_to_remove: Tuple = ("group_name", "project_name")
) -> Dict:
    """Removes the specified keys to avoid **args duplication in helper methods
    that receive dicts"""
    for key in keys_to_remove:
        kwargs.pop(key, None)
    return kwargs


def resolve_kwargs(
    kwargs: Dict,
    current_key: str = "group_name",
    old_key: str = "project_name",
) -> str:
    """Tries to get current_key from kwargs, with old_key as a fallback and
    raises an exception if none can be found"""
    try:
        return kwargs.get(current_key, kwargs.get(old_key))
    except KeyError:
        raise KeyError(
            f"Either {current_key} or {old_key} must be included, check "
            + "your query/mutation args!"
        )


def resolve_kwargs_key(
    kwargs: Dict,
    current_key: str = "group_name",
    old_key: str = "project_name",
) -> str:
    """Checks if either current_key or old_key exist in kwargs and returns the
    first of these keys, raises a KeyError otherwise"""
    if current_key in kwargs.keys():
        return current_key
    if old_key in kwargs.keys():
        return old_key
    raise KeyError(
        f"Couldn't find either {current_key} or {old_key} keys in the dict"
    )
