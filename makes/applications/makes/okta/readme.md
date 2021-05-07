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

# Special considerations or future improvements

- Work on decreasing api calls in order to avoid hiting API rate limits:
  https://github.com/okta/terraform-provider-okta/issues/186
- SWA apps do not support shared passwords yet, they are being managed manually:
  https://github.com/okta/terraform-provider-okta/issues/443
- Three Field apps do not support shared passwords yet, they are being managed manually:
  https://github.com/okta/terraform-provider-okta/issues/459
- SAML apps do not support app link configurations, they are being managed manually:
  https://github.com/okta/terraform-provider-okta/issues/461
- Some preconfigured auto_login apps are still pending migration as app settings must be passed:
  https://github.com/okta/terraform-provider-okta/issues/462
- AWS apps need some manual configuration after creation:
  https://support.okta.com/help/s/question/0D54z00006w0REiCAM/aws-account-federation-via-api?language=en_US
- Users must be created first on Okta and then on JumpCloud due to LDAP dependency.
- Custom apps do not support logos, they are being managed manually.
