---
id: graphql-api
title: GraphQL API
sidebar_label: GraphQL API
slug: /devs/integrates/graphql-api
---

## What is GraphQL?

>`GraphQL` is a query language for `APIs` and a runtime for fulfilling those queries with your
existing data. `GraphQL` provides a complete and understandable description of the data in
your `API`, gives clients the power to ask for exactly what they need and nothing more,
makes it easier to evolve `APIs` over time, and enables powerful developer tools.

— graphql.org

## Integrates GraphQL implementation

From late 2018 to mid-2019 we gradually migrated from a `REST`-like `API` to `GraphQL`,
first using [Graphene](https://graphene-python.org/), but since it didn't support ASGI and
async execution, in early 2020 we replaced it for `ariadne`.

Integrates currently uses the [ariadne](https://ariadnegraphql.org/) library,
developed by [Mirumee Labs](https://github.com/mirumee)

All `GraphQL` queries are directed to a
[single endpoint](https://gitlab.com/fluidattacks/product/-/blob/master/integrates/backend_new/app/app.py#L127),
which is exposed at `/api`.

The `API` layer was inspired by
[GitLab's GraphQL API](https://gitlab.com/gitlab-org/gitlab/tree/master/app/graphql)
and is structured in the following way:

```
api
|_ mutations
  |_ mutation_name.py
|_ resolvers
  |_ entity_name
    |_ field_resolver_name.py
|_ schema
  |_ enums
    |_ __init__.py <- Index for all enum bindings
    |_ enums.graphql <- GraphQL SDL declaring the available enums
  |_ scalars
    |_ __init__.py <- Index for all scalar bindings
    |_ scalars.graphql <- GraphQL SDL declaring the available scalars
  |_ types
    |_ type_name.py <- Type bindings
    |_ type_name.graphql <- GraphQL SDL type definition
```

### GraphQL Playground

The GraphQL Playground is a tool that allows to perform queries against the API or to explore the
schema definitions in a graphic and interactive way.
You can access it on:

- https://integrates.fluidattacks.com/api, which is production
- https://youruseratfluid.integrates.fluidattacks.com/api, which are the ephemerals
- https://localhost:8081/api, which is local

### Types

Integrates GraphQL types are defined in
[backend/api/schema/types](https://gitlab.com/fluidattacks/product/-/tree/master/integrates/back/packages/integrates-back/backend/api/schema/types)

There are two approaches to defining a `GraphQL` schema

1. Code-first
2. Schema-first

We use the latter, which implies defining the structure using `GraphQL SDL`
(Schema definition language) and binding it to python functions.

For example:

backend/api/schema/types/user.graphql
```
type User {
  email: String!
}
```

backend/api/schema/types/user.py
```py
from ariadne import ObjectType
from backend.api.resolvers.user import email

USER = ObjectType('User')

USER.set_field('email', email.resolve)
```

Further reading:

- [GraphQL docs - Schemas and Types](https://graphql.github.io/learn/schema/)
- [Mirumee blog - Schema-First GraphQL: The Road Less Travelled](https://blog.mirumee.com/schema-first-graphql-the-road-less-travelled-cf0e50d5ccff)

### Enums

Integrates GraphQL enums are defined in
[backend/api/schema/enums](https://gitlab.com/fluidattacks/product/-/tree/master/integrates/back/packages/integrates-back/backend/api/schema/enums)

backend/api/schema/enums/enums.graphql
```
enum AuthProvider {
  BITBUCKET
  GOOGLE
  MICROSOFT
}
```

> **_NOTE:_** By default, enum values passed to resolver functions will match their name

To map the value to something else, you can specify it in the enums binding index, for example:

backend/api/schema/enums/\__init__\.py
```py
from ariadne import EnumType

ENUMS: Tuple[EnumType, ...] = (
    ...,
    EnumType(
        'AuthProvider',
        {
            'BITBUCKET': 'bitbucket-oauth2',
            'GOOGLE': 'google-oauth2',
            'MICROSOFT': 'azuread-tenant-oauth2'
        }
    ),
    ...
)
```

### Scalars

Integrates GraphQL scalars are defined in
[backend/api/schema/scalars](https://gitlab.com/fluidattacks/product/-/tree/master/integrates/back/packages/integrates-back/backend/api/schema/scalars)

GraphQL provides some primitive scalars, such as String, Int and Boolean, but in some cases,
it is required to define custom ones that aren't included by default due to not (yet) being
part of the spec, like Datetime, JSON and Upload

Further reading:

- [Ariadne docs - Custom scalars](https://ariadnegraphql.org/docs/scalars)

### Resolvers

Integrates GraphQL resolvers are defined in
[backend/api/resolvers](https://gitlab.com/fluidattacks/product/-/tree/master/integrates/back/packages/integrates-back/backend/api/resolvers)

A resolver is a function that receives two arguments:

- **Parent:** The value returned by the parent resolver, usually a dictionary.
If it's a root resolver this argument will be None
- **Info:** An object whose attributes provide details about the execution
AST and the HTTP request.

It will also receive keyword arguments if the GraphQL field defines any.

backend/api/resolvers/user/email.py
```py
from graphql.type.definition import GraphQLResolveInfo

def resolve(parent: Any, info: GraphQLResolveInfo, **kwargs: Dict[str, Any]):
    return 'test@fluidattacks.com'
```

The function must return a value whose structure matches the type defined in the GraphQL schema

> **_IMPORTANT:_** Avoid reusing the resolver function. Other than the binding,
it should never be called in other parts of the code

Further reading:

- [Ariadne docs - resolvers](https://ariadnegraphql.org/docs/resolvers)

### Mutations

Integrates GraphQL mutations are defined in
[backend/api/mutations](https://gitlab.com/fluidattacks/product/-/tree/master/integrates/back/packages/integrates-back/backend/api/mutations)

Mutations are a kind of GraphQL operation explicitly meant to change data.

> **_NOTE:_** Mutations are also resolvers, just named differently for the sake of
separating concerns, and just like a resolver function, they receive the parent argument
(always None), the info object and their defined arguments

Most mutations only return `{'success': bool}` also known as "SimplePayload",
but they aren't limited to that. If you need your mutation to return other data,
just define the type in `backend/api/schema/types/mutation_payloads.graphql` and use it

backend/api/schema/types/mutation.graphql
```
type Mutation {
  createUser(email: String!): SimplePayload!
}
```

backend/api/mutations/create_user.py
```py
from graphql.type.definition import GraphQLResolveInfo

def mutate(parent: None, info: GraphQLResolveInfo, **kwargs: Dict[str, Any]):
    user_domain.create(kwargs['email'])
    return {'success': True}
```

backend/api/schema/types/mutation.py
```py
from ariadne import MutationType
from backend.api.mutations import create_user

MUTATION = MutationType()

MUTATION.set_field('createUser', create_user.mutate)
```

> **_IMPORTANT:_** Python code style prefers snake_case variables, so if the mutation receives
camelCased arguments, decorate the `mutate` function with the
`@convert_kwargs_to_snake_case decorator` from `ariadne.utils`

Further reading:

- [Ariadne docs - mutations](https://ariadnegraphql.org/docs/mutations)

### Errors

All exceptions raised, handled or unhandled will be reported in the "errors" field of the response

Raising exceptions can be useful to enforce business rules and report back to the client in
cases the operation could not be completed successfully

Further reading:

- https://spec.graphql.org/June2018/#sec-Errors

### Authentication

The Integrates API enforces authentication by checking for the presence and validity of a JWT
in the request cookies or headers

For resolvers or mutations that require authenticated users, decorate the function with the
`@require_login` from `backend.decorators`

### Authorization

The Integrates API enforces authorization implementing an ABAC model.

There are currently three levels of authorization

- User
- Organization
- Group

The system then validates if the user can perform the action in a certain authz level according
to the policies defined in
[backend/authz/model.py](https://gitlab.com/fluidattacks/product/-/tree/master/integrates/back/packages/integrates-back/backend/authz/model.py)

For resolvers or mutations that require authorized users, decorate the function with the
appropriate decorator from `backend.decorators`

- @enforce_user_level_auth_async
- @enforce_organization_level_auth_async
- @enforce_group_level_auth_async

## Performance optimizations

In order to make the API more performant, we are moving towards a fully async backend.
For better comprehension on how it's done in python, here's an article that provides a
good explanation:
[Writing fast and concurrent code, even at architectural windward](/devs/integrates/writing-code-suggestions)

### Implementing and using dataloaders

Work in progress, please check back later

### Caching resolvers

Work in progress, please check back later

## Guides

### Adding new fields

Work in progress, please check back later

1. Declare the field in the schema using SDL
2. Write the resolver function
3. Bind the resolver function to the schema


### Deprecation and removal of fields

Unlike REST-like APIs, [GraphQL encourages to avoid versioning](https://graphql.org/learn/best-practices/#versioning),
but there are still some things to keep in mind in order to avoid disruptions while evolving the APs.

Our current policy mandates removal 6 months after marking the field as deprecated.

To mark fields or enums as deprecated, use the
[`@deprecated` directive](https://spec.graphql.org/June2018/#sec-Field-Deprecation), e.g:
```
type ExampleType {
  oldField: String @deprecated(reason: "reason text")
}
```

#### Deprecation reason guidelines

The reason should follow something similar to:
```
This {field|mutation} is deprecated and will be removed after {date}.
```

If it was replaced or there is an alternative, it should include: 
```
Use the {alternative} {field|mutation} instead.
```

### Testing

Work in progress, please check back later