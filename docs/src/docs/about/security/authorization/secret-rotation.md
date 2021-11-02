---
id: secret-rotation
title: Secret Rotation
sidebar_label: Secret Rotation
slug: /about/security/authorization/secret-rotation
---

[Key rotation](/criteria/requirements/130) is essential
when dealing with sensitive data.
The best way to prevent key leakage
is by changing keys regularly.
Our rotation cycles are as follows:

- **KMS keys:** every year or earlier if necessary

- **JWT tokens:** daily

- **Digital certificates:** every 30 days

- **IAM passphrases:** [every three months](/criteria/requirements/089)

We make rotations in the following two ways:

- **Automatic rotation:**
  Some secrets are stored in secret vaults.
  They are only accessible by administrators
  and are rotated daily.
  These secrets include JWT tokens,
  IAM passphrases
  and digital certificates.

- **Manual rotation:**
  Some secrets are stored versioned
  and encrypted in git repositories
  using AES256 symmetric keys.
  They are treated as code,
  which means that
  [manual approval](https://fluidattacks.com/about/security/#PR)
  is required to rotate them.
  These secrets include KMS keys
  and other application credentials.
