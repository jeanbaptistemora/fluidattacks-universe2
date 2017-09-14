class IntercomCustomData(object):
    """ Custom data class."""

    def custom_data(self, user):
        """Send extra data to Intercom."""

        name = user.get_full_name()

        return {
            'name' : name,
        }
