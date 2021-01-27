# Cache Design

- Why? because of performance. More in the issues:
  - https://gitlab.com/fluidattacks/product/-/issues/3985
  - https://gitlab.com/fluidattacks/product/-/issues/2988
- Redis Constraints:
  - Redis is a key-value store, O(1) complexity (fast) for single-key commands
    and O(num-of-keys-stored-in-all-shards) complexity (slow) for
    multiple-key commands like patterns (`test*`)
  - Redis accepts keys as strings, and values as bytes/strings
- Back-end Constraints:
  - The back-end needs to store arbitrary python objects like dictionaries,
    lists, containers, dates, etc
  - The back-end needs to invalidate recursively object relations
  - We don't want to spread the cache logic over all the back-end (maintainability)
- Solution:
  - GET/SET(EX)/DEL/TTL/EXPIRE are the only commands allowed.
    In other words, all commands target 1 and only 1 key
  - We use a model which abstracts object relations
  - We serialize values using a library similar to JSON, extended for objects
    that JSON do not support like NamedTuples, Decimal, datetime, etc
- Implementation:
  - There is a model that comprises top-level entities and their attributes
    as well as the arguments that make the entity unique. The actions that
    should invalidate the entity cache are documented in the dependencies set.

    Note that the same dependency may appear in many entities:

    ```py
    ENTITIES: Dict[str, Dict[str, Set[str]]] = dict(
        event=dict(
            args={
                'id',
            },
            attrs={
                'consulting',
            },
            dependencies={
                'add_event_consult',
                'handle_vulns_acceptation',
                'test',
            },
        ),
        finding=dict(
            args={
                'id',
            },
            attrs={
                # ...
                'inputs_vulns',
                'last_vulnerability',
                'lines_vulns',
                # ...
            },
            dependencies={
                # ...
                'reject_draft',
                'reject_zero_risk_vuln',
                'request_verification_vulnerability',
                'test',
                # ...
            },
        ),
      }
    ```

    You can cache the value of an attribute corresponding to an entity:

    ```py
    await redis_set_entity_attr(
      entity='finding',
      attr='last_vulnerability',
      id='123123',
      value=ComplexPythonObject,
    )

    # Redis Key: finding.vulns@id=949824826
    # Redis Value (a byte-string representing the ComplexPythonObject):
    #   [["builtins","list"],[[["builtins","dict"],[[[["builtins","str"],
    #   ["UUID"],{}],[["builtins","str"],["7a4f6881-
    #   ....
    ```

    You can retrieve such value:

    ```py
    assert ComplexPythonObject == await redis_get_entity_attr(
        entity='finding',
        attr='last_vulnerability',
        id='123123',
    )
    ```

    You can cache a generator function that computes the value:

    ```py
    async def generator_function(*args, **kwargs):
        return await db()

    await redis_get_or_set_entity_attr(
        partial(generator_function, *args, **kwargs),
        entity='finding',
        attr='last_vulnerability',
        id='123123',
    )
    ```

    You can invalidate the cache by dependencies. This will automatically
    invalidate all entries in the cache for the entities that depend on
    _test_, in this case event and finding:

    ```py
    await redis_del_by_deps('test', event_id='123123', finding_id='123123')
    ```

    If a consistent write is not important you can delay the invalidation
    to be executed in the near-future with:

    ```py
    redis_del_by_deps_soon('test', event_id='123123', finding_id='123123')
    ```

    This makes the request faster to the user, but changes may take a little
    to be applied (this is acceptable in most scenarios)

- Results:
  - Fast, generic, maintainable, correct caching system
