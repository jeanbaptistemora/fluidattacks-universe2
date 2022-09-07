# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

"""
This migration updates the value of the provider in Django's social_auth table
of all the users that authenticate to the platform using the Azure button.

It is necessary so the new provider can resolve existing users and does not
end up creating duplicate ones.

Execution Time: 2020-06-02 14:32:00 UTC-5
Finalitzation Time: 2020-06-02 14:35:00 UTC-5
"""

import django
import os

django.setup()


from social_django.models import UserSocialAuth  # pylint: disable-all

STAGE: str = os.environ["STAGE"]


def main() -> None:
    if STAGE == "test":
        users_to_update = UserSocialAuth.objects.filter(
            provider="azuread-oauth2"
        )
        print(f"{len(users_to_update)} users to update:")
        for user in users_to_update:
            print(f"\tUser {user} will be updated...")
    else:
        UserSocialAuth.objects.filter(provider="azuread-oauth2").update(
            provider="azuread-tenant-oauth2"
        )


if __name__ == "__main__":
    main()
