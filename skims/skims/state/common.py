# Standard library
from os.path import (
    join,
)
from typing import (
    Any,
    Optional,
)

# Third party libraries
import aiofiles

# Local libraries
from serialization import (
    dump as py_dumps,
    load as py_loads,
)
from utils.crypto import (
    get_hash,
)


async def get_obj_id(obj: Any) -> bytes:
    """Compute an unique identifier from a Python object.

    :param obj: The object to identify
    :type obj: Any
    :return: An unique object identifier
    :rtype: bytes
    """
    return await get_hash(await py_dumps(obj))


async def read_blob(obj_location: str) -> Any:
    async with aiofiles.open(  # type: ignore
        obj_location, mode='rb',
    ) as obj_store:
        obj_stream: bytes = await obj_store.read()
        return await py_loads(obj_stream)


async def retrieve_object(folder: str, key: Any) -> Any:
    """Retrieve an entry from the cache.

    :param folder: Path to folder to retrieve data from
    :type folder: str
    :param key: Key that identifies the value to be read
    :type key: Any
    :return: The value that is hold under the specified key
    :rtype: Any
    """
    obj_id: bytes = await get_obj_id(key)
    obj_location: str = join(folder, obj_id.hex())

    return await read_blob(obj_location)


async def store_object(
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
    obj_id: bytes = await get_obj_id(key)
    obj_stream: bytes = await py_dumps(value, ttl=ttl)
    obj_location: str = join(folder, obj_id.hex())

    async with aiofiles.open(  # type: ignore
        obj_location, mode='wb',
    ) as obj_store:
        await obj_store.write(obj_stream)
