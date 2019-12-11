from graphene import Schema
from backend.api.query import Query
from backend.api.mutations import Mutations


SCHEMA = Schema(query=Query, mutation=Mutations, types=[])
