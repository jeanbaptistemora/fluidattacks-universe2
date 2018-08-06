# pylint: disable=F0401
from app.dao import integrates_dao
from graphene import Boolean, ObjectType

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

    #pylint: disable=unused-argument
    def resolve_authorized(self, info):
        """ Resolve user authorization """
        return self.authorized

    #pylint: disable=unused-argument
    def resolve_remember(self, info):
        """ Resolve remember preference """
        return self.remember
