def is_action_permissive(action: str) -> bool:
    if not isinstance(action, str):
        # A var or syntax error
        return False

    splitted = action.split(':', 1)  # a:b
    provider = splitted[0]  # a
    effect = splitted[1] if splitted[1:] else None  # b

    return (
        (provider == '*')
        or (effect and effect.startswith('*'))
        or ('*' in provider and effect is None)
    )


def is_resource_permissive(resource: str) -> bool:
    if not isinstance(resource, str):
        # A var or syntax error
        return False

    return (
        # Consider adding here arn:aws:iam::* and derivatives
        (resource == '*')
    )
