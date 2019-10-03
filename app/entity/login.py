from graphene import Boolean, ObjectType, Mutation

# pylint: disable=no-self-use
# pylint: disable=super-init-not-called
# pylint: disable=F0401
from app.domain import user as user_domain
from app.util import get_jwt_content


class Login(ObjectType):
    # declare attributes
    authorized = Boolean()
    remember = Boolean()

    def __init__(self, user_email):
        """ Login information class """
        self.authorized = user_domain.is_registered(user_email)
        user_info = user_domain.get_user_attributes(
            user_email, ['legal_remember'])
        self.remember = user_info['legal_remember'] if user_info else False

    def resolve_authorized(self, info):
        """ Resolve user authorization """
        del info
        return self.authorized

    def resolve_remember(self, info):
        """ Resolve remember preference """
        del info
        return self.remember


class AcceptLegal(Mutation):
    class Arguments(object):
        remember = Boolean()
    success = Boolean()

    def mutate(self, info, remember):
        user_email = get_jwt_content(info.context)['user_email']
        is_registered = user_domain.is_registered(user_email)

        if is_registered:
            user_domain.update_legal_remember(user_email, remember)
            success = True
        else:
            success = False

        return AcceptLegal(success=success)
