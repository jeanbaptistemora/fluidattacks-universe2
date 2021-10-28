---
id: encryption-rest
title: Encryption at Rest
sidebar_label: Encryption at Rest
slug: /about/security/confidentiality/encryption-rest
---

All our applications and services
have industry-standard
[encryption at rest](/criteria/requirements/224).

- All the sensitive data
  provided by our clients
  (repository access keys, VPN credentials, etc.)
  is encrypted
  using the symmetric algorithm of our key management system (KMS).
  This algorithm is based on Advanced Encryption Standard (AES)
  in Galois Counter Mode (GCM)
  with [256-bit](/criteria/requirements/150)
  [private keys](/criteria/requirements/145).
  AES256 is the
  [US government standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
  encryption algorithm used to protect top-secret information.
  Additionally,
  client data is also protected using
  [HMAC](https://en.wikipedia.org/wiki/HMAC)
  with [SHA-256](https://en.wikipedia.org/wiki/SHA-2) hashes.

- All our domain names are protected with
  [DNSSEC](https://www.icann.org/resources/pages/dnssec-what-is-it-why-important-2019-03-05-en)
  to ensure that DNS records
  received by clients
  are identical to the DNS records
  published by us.

- All our clients' code repositories are stored in private,
  [AES256 ciphered](/criteria/requirements/185)
  redundant data centers.

- Our exploits are stored encrypted
  using AES256 keys.

- All [Attack Surface Manager (ASM)](https://app.fluidattacks.com/)
  data is stored in an AES256 encrypted database.

- Most of our encrypted-at-rest secrets are only decrypted in memory,
  meaning that
  they are never stored on a hard drive when decrypted.
  This highly reduces the possibility of a data leakage
  caused by leaving unprotected files
  with decrypted secrets
  stored on hard drives.

- All our products use our KMS
  for both development and production secrets.

- All our Windows laptops have their hard drives encrypted
  using Bitlocker.
  A domain controller continuously checks adherence
  to this policy.

- All our Linux laptops have their hard drives encrypted
  from the bootloader
  using LUKS.
