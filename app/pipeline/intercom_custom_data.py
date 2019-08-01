# pylint: disable=E0402
from ..dal import integrates_dal


# pylint: disable=no-self-use
class IntercomUserData(object):
    def user_data(self, user):
        """ Required method, same name and only accepts
            one attribute (django User model) """
        name = user.get_full_name()
        email = user.get_username()
        return {
            'name': name,
            'email': email,
        }


class IntercomCustomData(object):
    """ Custom data class. """
    def custom_data(self, user):
        """ Send extra data to Intercom. """
        email = user.get_username()
        company = integrates_dal.get_organization(email)
        return {
            'Company': company,
        }
