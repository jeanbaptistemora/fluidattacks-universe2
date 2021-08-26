# What

This module contains our entire Okta ecosystem written as code.

# Why

1. Full reproducibility
2. Full traceability
3. Full manageability

# How

We use several technologies for accomplishing this:

1. SOPS and KMS for encrypting all our Okta data (apps, groups, users, etc).
2. Python for parsing the data.
3. Terraform and okta provider for implementing the infrastructure.

# Contributing

1. In order to be able to open de data file, you need `makes_prod` access.
2. All jobs can be normally ran with `m . <job>`.

## Recommendations

1. Avoid assigning apps directly to users as much as you can,
  this makes permissions management complexity to exponentially increase.
2. The less groups you have, the better.
  Try to make everyone fit in a small set of groups,
  this will simplify permissions management.
3. If you're testing an app and auto-assign it,
  remember to remove yourself after testing is complete.
4. Follow conventions:
   1. `id`'s for all entities should only be composed of: `a-z` and `_`.
   2. If the same app exists for two or more companies, use: `<APP> - <COMPANY>`.
   3. If the same app exists for two or more users, use `<APP> - <USER>`.
   4. If the same app exists for two or more companies and users, use `<APP> - <COMPANY> - <USER>`.

# Special considerations or future improvements

- Work on decreasing api calls in order to avoid hiting API rate limits:
  https://github.com/okta/terraform-provider-okta/issues/186.
- RADIUS applications are not supported, they are being managed manually:
  https://github.com/okta/terraform-provider-okta/issues/475
- Three Field apps do not support shared passwords yet, they are being managed manually:
  https://github.com/okta/terraform-provider-okta/issues/458.
- Auto Login apps do not support app link configurations, they are being managed manually:
  https://github.com/okta/terraform-provider-okta/issues/608.
- AWS apps need some manual configuration after creation:
  https://support.okta.com/help/s/question/0D54z00006w0REiCAM/aws-account-federation-via-api?language=en_US.
