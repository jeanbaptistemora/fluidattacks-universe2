---
id: secret-rotation
title: Secret rotation
sidebar_label: Secret rotation
slug: /security/authorization/secret-rotation
---

[Key rotation](https://fluidattacks.com/products/rules/list/130/) is essential when dealing
with sensitive data. The best way to prevent a key leakage is by changing the keys regularly.
Our rotation cycles are as follows:

- **KMS keys:** every year or before in case it is needed.

- **JWT Tokens:** daily.

- **Digital Certificates:** every three months.

- **IAM passphrases:** [every three months](https://fluidattacks.com/products/rules/list/089/).

Rotations are done in these two different ways:

- **Automatic rotation:** Some secrets are stored in secret vaults. They are only accessible
by administrators and are rotated daily. These secrets include JWT Tokens, IAM passphrases,
and digital certificates.

- **Manual rotation:** Some secrets are stored versioned and encrypted in git repositories
using AES256 symmetric keys. They are treated as code, meaning that to be rotated a
[manual approval](https://fluidattacks.com/security/#PR) needs to be obtained.
These secrets include KMS keys and other application credentials.
