from datetime import datetime, timedelta
from graphene import Boolean, ObjectType, Mutation, String

# pylint: disable=no-self-use
# pylint: disable=super-init-not-called
# pylint: disable=F0401
from django.conf import settings
from app.dao import integrates_dao
from app.util import get_jwt_content
from jose import jwt


class Login(ObjectType):
    # declare attributes
    authorized = Boolean()
    remember = Boolean()
    auth_jwt = String()

    def __init__(self, user_email, session):
        """ Login information class """
        self.authorized = integrates_dao.is_registered_dao(user_email) == '1'
        user_info = integrates_dao.get_user_dynamo(user_email)
        self.remember = False
        if not user_info == []:
            user_info = dict(user_info[0])
            if "legal_remember" in user_info:
                self.remember = user_info["legal_remember"]
                session['accept_legal'] = self.remember

    def resolve_authorized(self, info):
        """ Resolve user authorization """
        del info
        return self.authorized

    def resolve_remember(self, info):
        """ Resolve remember preference """
        del info
        return self.remember

    def resolve_auth_jwt(self, info):
        token = jwt.encode(
            {
                'user_email': info.context.session['username'],
                'user_role': info.context.session['role'],
                'exp': datetime.utcnow() + timedelta(
                    seconds=settings.SESSION_COOKIE_AGE)
            },
            algorithm='HS512',
            key=settings.JWT_SECRET,
        )
        self.auth_jwt = token
        return self.auth_jwt


class AcceptLegal(Mutation):
    class Arguments(object):
        remember = Boolean()
    success = Boolean()

    def mutate(self, info, remember):
        user_email = get_jwt_content(info.context)["user_email"]
        is_registered = integrates_dao.is_registered_dao(user_email) == '1'

        if is_registered:
            integrates_dao.update_legal_remember_dynamo(
                user_email,
                remember
            )
            success = True
        else:
            success = False

        info.context.session['accept_legal'] = success
        return AcceptLegal(success=success)
