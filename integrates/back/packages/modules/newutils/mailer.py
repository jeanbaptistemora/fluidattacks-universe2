from backend.dal import user as user_dal


async def get_recipient_first_name(email: str) -> str:
    first_name = email.split('@')[0]
    user_attr = await user_dal.get_attributes(email, ['first_name'])
    if user_attr and user_attr.get('first_name'):
        first_name = user_attr['first_name']
    return str(first_name)
