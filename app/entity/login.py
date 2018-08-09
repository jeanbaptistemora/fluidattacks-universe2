# pylint: disable=F0401
from app.dao import integrates_dao
from graphene import Boolean, ObjectType, Mutation

class Login(ObjectType):
    # declare attributes
    authorized = Boolean()
    remember = Boolean()

    def __init__(self, user_email, session):
        """ Login information class """
        self.authorized = integrates_dao.is_registered_dao(user_email) == '1'
        userInfo = integrates_dao.get_user_dynamo(user_email)
        self.remember = False
        if not userInfo == []:
            userInfo = dict(userInfo[0])
            if "legal_remember" in userInfo:
                self.remember = userInfo["legal_remember"]
                session['accept_legal'] = True

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

    @classmethod
    def mutate(self, args, info, remember):
        del args
        username = info.context.session['username']

        integrates_dao.update_legal_remember_dynamo(
            username,
            remember
        )

        info.context.session['accept_legal'] = True
        return AcceptLegal(success=True)
