---
id: internal
title: Internal
sidebar_label: Internal
slug: /about/security/authentication/internal
---

## Centralized authentication

We use a centralized authentication platform (IAM)
to manage all our internal applications.
Our employees do not know
any of the passwords
of the managed applications;
they only know their own IAM passphrases.
Once they log in to IAM,
they can access the applications
[assigned to them](/criteria/requirements/096).

Some of our IAM specifications
and requirements are listed below:

- We use
  [passphrases instead of passwords](/criteria/requirements/132)
  (more information [here](https://fluidattacks.com/blog/requiem-password/)).

- [Passphrases expire every 30 days](/criteria/requirements/130).

- We can only reuse previous passphrases
  after a [24 reset cycle](/criteria/requirements/129).

- We must set up
  [multi-factor authentication](/criteria/requirements/328) (MFA)
  from mobile devices.

- Our MFA uses
  [OOB](/criteria/requirements/153),
  a mechanism that transports all the MFA data
  through a different channel
  than the application's channel itself.
  Text messages and emails are examples of OOB.
  It reduces the risk
  in case a communication channel becomes compromised.

- We use both
  [SAML](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language)
  and [Oauth2](https://oauth.net/2/)
  for authentication.
  These two protocols allow us to log in
  to external applications
  with only our IAM active account.
  No passwords or users are needed.

- In case a mobile phone supports
  [biometric authentication](/criteria/requirements/231),
  our IAM enforces its usage.

- All successful sessions have a duration of 9 hours.

## GPG signature for repository commits

In order to prevent identity hijacking,
all our source code repositories require developers
to use a
[GPG digital signature](https://en.wikipedia.org/wiki/GNU_Privacy_Guard)
that verifies the developer's identity
on the Internet.
The signatures can be found
in the repository commit histories
linked in the
[Open Source section](../transparency/open-source).
