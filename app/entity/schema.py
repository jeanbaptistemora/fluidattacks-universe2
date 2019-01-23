from graphene import Schema
from .query import Query
from .mutations import Mutations


SCHEMA = Schema(query=Query, mutation=Mutations, types=[])
