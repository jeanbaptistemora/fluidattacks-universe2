# Standard library
from os.path import (
    join,
)
from typing import (
    Any,
    Optional,
)

# Local libraries
from serialization import (
    dump as py_dumps,
    load as py_loads,
)
from utils.crypto import (
    get_hash,
)


def get_obj_id(obj: Any) -> bytes:
    """Compute an unique identifier from a Python object.

    :param obj: The object to identify
    :type obj: Any
    :return: An unique object identifier
    :rtype: bytes
    """
    return get_hash(py_dumps(obj))


def read_blob(obj_location: str) -> Any:
    with open(obj_location, 'rb') as obj_store:
        obj_stream: bytes = obj_store.read()
        return py_loads(obj_stream)


def retrieve_object(folder: str, key: Any) -> Any:
    """Retrieve an entry from the cache.

    :param folder: Path to folder to retrieve data from
    :type folder: str
    :param key: Key that identifies the value to be read
    :type key: Any
    :return: The value that is hold under the specified key
    :rtype: Any
    """
    obj_id: bytes = get_obj_id(key)
    obj_location: str = join(folder, obj_id.hex())

    return read_blob(obj_location)


def store_object(
    folder: str,
    key: Any,
    value: Any,
    ttl: Optional[int] = None,
) -> None:
    """Store an entry in the cache.

    :param folder: Path to folder to store data into
    :type folder: str
    :param key: Key under the value is to be aliased
    :type key: Any
    :param value: Value to store
    :type value: Any
    :param ttl: Time to live in seconds, defaults to None
    :type ttl: Optional[int], optional
    """
    obj_id: bytes = get_obj_id(key)
    obj_stream: bytes = py_dumps(value, ttl=ttl)
    obj_location: str = join(folder, obj_id.hex())

    with open(obj_location, 'wb') as obj_store:
        obj_store.write(obj_stream)
