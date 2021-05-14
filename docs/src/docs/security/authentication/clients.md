---
id: clients
title: For clients
sidebar_label: For clients
slug: /security/authentication/clients
---

[Attack Surface Manager (ASM)](https://app.fluidattacks.com/)
only uses
[SSO](https://en.wikipedia.org/wiki/Single_sign-on)
with Bitucket, Google and Microsoft Accounts.
[Oauth2](https://oauth.net/2/) protocol is used.
Such protocol only accepts login attempts from trusted URLs
and has industry-standard 2048 bytes access tokens.
We do not store any account passwords.
The only personal information we store of our clients is:

- Full name (provided by Google or Microsoft)

- Company and cellphone (only if shared, user can decide)

It is also worth noting
that if users lose their corporate email,
[they also lose access](/criteria/authorization/114)
to their
[Attack Surface Manager (ASM)](https://app.fluidattacks.com/)
account.
Clients can [easily manage](/criteria/authorization/034)
who has and who does not have
access to their projects.
