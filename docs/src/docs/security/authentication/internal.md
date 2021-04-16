---
id: internal
title: Internal
sidebar_label: Internal
slug: /security/authentication/internal
---

## Centralized authentication
We use a centralized authentication platform (IAM) to manage all the applications we
internally use. Our employees do not know any of the passwords of the managed applications;
they only know their own IAM passphrase. Once they log in to IAM, they can access applications
[assigned to them](https://fluidattacks.com/products/rules/list/096/).

Some of our IAM specifications and requirements are listed below:

- [Passphrases instead of passwords](https://fluidattacks.com/products/rules/list/132/)
(more information [here](https://fluidattacks.com/blog/requiem-password/)).

- [Passphrases expire every 30 days](https://fluidattacks.com/products/rules/list/130/).

- Previous passphrases can only be reused after a
[24 reset cycle](https://fluidattacks.com/products/rules/list/129/).

- [Multi-factor authentication](https://fluidattacks.com/products/rules/list/328/) (MFA)
from a mobile device must be set.

- Our MFA uses [OOB](https://fluidattacks.com/products/rules/list/153/), a mechanism that
transports all the MFA data through a different channel than the application’s channel itself.
Text messages and emails are examples of OOB. It reduces the risk in case a communication
channel becomes compromised.

- We use both [SAML](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) and
[Oauth2](https://oauth.net/2/) for logging in. These two protocols allow us to log in to external
applications by only having our IAM active account. No passwords or users are needed.

- In case a mobile phone supports
[biometric authentication](https://fluidattacks.com/products/rules/list/231/),
our IAM enforces its usage.

- All successful sessions have a duration of 9 hours.

## GPG signature for repository commits
In order to avoid identity hijacking, all our source code repositories require developers to use a
[GPG digital signature](https://en.wikipedia.org/wiki/GNU_Privacy_Guard) that verifies the
developer’s identity on the Internet. Signatures can be found on the repository commit histories
linked in the [Open Source section](https://fluidattacks.com/security/#open-source).
