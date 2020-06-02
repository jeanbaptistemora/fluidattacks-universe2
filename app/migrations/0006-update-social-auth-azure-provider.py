"""
This migration updates the value of the provider in Django's social_auth table
of all the users that authenticate to the platform using the Azure button.

It is necessary so the new provider can resolve existing users and does not
end up creating duplicate ones.
"""

import os

import django


django.setup()


from social_django.models import UserSocialAuth


STAGE: str = os.environ['STAGE']


def main() -> None:
    if STAGE == 'test':
        users_to_update = UserSocialAuth.objects.filter(provider='azuread-oauth2')
        print('{} users to update:'.format(len(users_to_update)))
        for user in users_to_update:
            print('\tUser {} will be updated...'.format(user))
    else:
        UserSocialAuth.objects.filter(provider='azuread-oauth2').update(provider='azuread-tenant-oauth2')


if __name__ == '__main__':
    main()
