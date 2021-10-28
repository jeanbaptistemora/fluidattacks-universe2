---
id: clients
title: For Clients
sidebar_label: For Clients
slug: /about/security/authentication/clients
---

The [Attack Surface Manager (ASM)](https://app.fluidattacks.com/)
only uses [SSO](https://en.wikipedia.org/wiki/Single_sign-on)
with Bitbucket,
Google and Microsoft Accounts.
[Oauth2](https://oauth.net/2/) protocol is used.
Such protocol
only accepts login attempts
from trusted URLs
and has industry-standard 2048 bytes access tokens.
We do not store any account passwords.
The only personal information we store about our clients is the following:

- Full name (provided by Google or Microsoft)

- Company name and cell phone number
  (only if the user chooses to share them)

It is worth noting that
if users lose their corporate email,
[they also lose access](/criteria/requirements/114)
to their ASM account.
In addition,
customers can [easily manage](/criteria/requirements/034)
who does
and who does not have access
to their projects.
