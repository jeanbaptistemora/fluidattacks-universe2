from graphene import Schema
from api.query import Query
from api.mutations import Mutations


SCHEMA = Schema(query=Query, mutation=Mutations, types=[])
