from app.dal import user as user_dal


def add_phone_to_user(email, phone):
    """ Update user phone number. """
    return user_dal.update_user_attribute(email, phone, 'phone')


def get_user_attributes(email, data):
    """ Get attributes of a user. """
    return user_dal.get_user_attributes(email, data)


def update_legal_remember(email, remember):
    """ Remember legal notice acceptance """
    return user_dal.update_user_attribute(email, remember, 'legal_remember')


def update_access_token(email, session_jwt):
    """ Update access token """
    return user_dal.update_user_attribute(email, session_jwt, 'access_token')
