from backend.dal import available_group as available_group_dal


async def exists(group_name: str) -> bool:
    return await available_group_dal.exists(group_name)


async def get_name() -> str:
    return await available_group_dal.get_one()


async def remove(group_name: str) -> bool:
    return await available_group_dal.remove(group_name)
