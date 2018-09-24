from .query import Query
from .mutations import Mutations
from graphene import Schema

schema = Schema(query=Query, mutation=Mutations)
