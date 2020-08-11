def get_cached_group_service_attributes_policies(
    group: str,
) -> Tuple[Tuple[str, str], ...]:
    """Cached function to get 1 group features authorization policies."""
    cache_key: str = get_group_cache_key(group)

    try:
        # Attempt to retrieve data from the cache
        ret = cache.get(cache_key)
    except RedisClusterException:
        ret = None

    if ret is None:
        # Let's fetch the data from the database
        ret = tuple(
            (policy.group, policy.service)
            for policy in project_dal.get_service_policies(group))
        try:
            # Put the data in the cache
            cache.set(cache_key, ret, timeout=3600)
        except RedisClusterException:
            # asdf
            pass

    return cast(Tuple[Tuple[str, str], ...], ret)
