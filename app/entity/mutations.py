from .login import AcceptLegal
from graphene import ObjectType

class Mutations(ObjectType):
    acceptLegal = AcceptLegal.Field()
