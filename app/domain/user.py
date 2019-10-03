from app.dal import user as user_dal


def add_phone_to_user(email, phone):
    """ Update user phone number. """
    return user_dal.update_user_attribute(email, phone, 'phone')


def get_role(email):
    """ Get the role of a user. """
    return user_dal.get_role(email)


def get_user_attributes(email, data):
    """ Get attributes of a user. """
    return user_dal.get_user_attributes(email, data)


def is_registered(email):
    is_registered_attr = get_user_attributes(email, ['registered'])
    registered = False
    if is_registered_attr and is_registered_attr.get('registered') == 1:
        registered = True
    else:
        # User not found or registered attr is 0
        pass
    return registered


def register(email):
    return user_dal.update_user_attribute(email, 1, 'registered')


def remove_access_token(email):
    """ Remove access token attribute """
    return user_dal.remove_user_attribute(email, 'access_token')


def update_legal_remember(email, remember):
    """ Remember legal notice acceptance """
    return user_dal.update_user_attribute(email, remember, 'legal_remember')


def update_access_token(email, token_data):
    """ Update access token """
    access_token = {
        'jti': token_data['jti_hashed'],
        'salt': token_data['salt']
    }
    return user_dal.update_user_attribute(email, access_token, 'access_token')
