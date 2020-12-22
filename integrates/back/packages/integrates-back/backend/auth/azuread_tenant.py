from social_core.backends.azuread_tenant import AzureADTenantOAuth2


# pylint: disable=abstract-method, too-few-public-methods
class AzureADTenantBackend(AzureADTenantOAuth2):
    """ https://github.com/python-social-auth/social-core/issues/450 """

    def get_user_id(self, details, response):
        return response.get('upn')

    def user_data(self, access_token, *args, **kwargs):
        response = kwargs.get('response')
        if response is None:
            kwargs.update({'response': {'id_token': access_token}})

        return super(AzureADTenantBackend, self).user_data(
            access_token, *args, **kwargs)
