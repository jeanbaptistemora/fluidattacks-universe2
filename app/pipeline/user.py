from ..dao import integrates_dao


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        print ("User %s is already on DB" % (user,))
        integrates_dao.update_user_login_dao(user)
        return

    username = details['username']
    first_name = details['first_name']
    last_name = details['last_name']
    email = details['email']

    integrates_dao.create_user_dao(username, first_name, last_name, email)
