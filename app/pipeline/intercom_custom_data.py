# pylint: disable=relative-beyond-top-level
from ..domain import user as user_domain


# pylint: disable=no-self-use
class IntercomUserData():
    def user_data(self, user):
        """ Required method, same name and only accepts
            one attribute (django User model) """
        name = user.get_full_name()
        email = user.get_username()
        return {
            'name': name,
            'email': email,
        }


class IntercomCustomData():
    """ Custom data class. """
    def custom_data(self, user):
        """ Send extra data to Intercom. """
        email = user.get_username()
        company = user_domain.get_data(email, 'company')
        return {
            'Company': company,
        }
