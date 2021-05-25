from names import dal as names_dal


async def create(name: str, entity: str) -> bool:
    return await names_dal.create(name, entity)


async def exists(name: str, entity: str) -> bool:
    return await names_dal.exists(name, entity)


async def get_name(entity: str) -> str:
    return await names_dal.get_one(entity)


async def remove(name: str, entity: str) -> bool:
    return await names_dal.remove(name, entity)
