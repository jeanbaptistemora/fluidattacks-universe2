from backend.dal import available_name as available_name_dal


async def exists(name: str, entity: str) -> bool:
    return await available_name_dal.exists(name, entity)


async def get_name(entity: str) -> str:
    return await available_name_dal.get_one(entity)


async def remove(name: str, entity: str) -> bool:
    return await available_name_dal.remove(name, entity)
