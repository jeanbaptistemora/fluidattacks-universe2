from graphene import Schema
from app.api.query import Query
from app.api.mutations import Mutations


SCHEMA = Schema(query=Query, mutation=Mutations, types=[])
