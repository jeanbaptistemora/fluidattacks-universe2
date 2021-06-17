---
id: cipher-suites
title: Cipher Suites
sidebar_label: Cipher Suites
slug: /criteria/vulnerabilities/052/details/cipher-suites
---

A cipher suite is a set of algorithms
that help secure a network connection.
Suites typically use Transport Layer Security (TLS)
or its now-deprecated predecessor Secure Socket Layer (SSL).
The set of algorithms
that cipher suites usually contain include:
a key exchange algorithm,
a bulk encryption algorithm,
and a message authentication code (MAC) algorithm.

The **key exchange algorithm**
is used to exchange a key between two devices.
This key is used to encrypt and decrypt the messages
being sent between two machines.

The **bulk encryption algorithm**
is used to encrypt the data being sent.

The **MAC algorithm**
provides data integrity checks
to ensure that the data sent
does not change in transit.
In addition,
cipher suites can include signatures
and an authentication algorithm
to help authenticate the server and or client.

A cipher suite is as secure
as the algorithms that it contains.
If the version of encryption
or authentication algorithm in a cipher suite
have known vulnerabilities,
the cipher suite and TLS connection is then vulnerable.

## Weak algorithms

- **RSA with key < 2048 bytes**,
  can be brute-forced in feasible time

- **OpenSSL Elliptic Curves**, secp112r1, secp112r2, secp128r1, secp128r2,
  secp160k1, secp160r1, secp160r2, secp192k1, prime192v1, prime192v2,
  prime192v3, sect113r1, sect113r2, sect131r1, sect131r2, sect163k1, sect163r1,
  sect163r2, sect193r1, sect193r2, c2pnb163v1, c2pnb163v2, c2pnb163v3,
  c2pnb176v1, c2tnb191v1, c2tnb191v2, c2tnb191v3, c2pnb208w1,
  wap-wsg-idm-ecid-wtls1, wap-wsg-idm-ecid-wtls3, wap-wsg-idm-ecid-wtls4,
  wap-wsg-idm-ecid-wtls5, wap-wsg-idm-ecid-wtls6, wap-wsg-idm-ecid-wtls7,
  wap-wsg-idm-ecid-wtls8, wap-wsg-idm-ecid-wtls9, wap-wsg-idm-ecid-wtls10,
  wap-wsg-idm-ecid-wtls11, oakley-ec2n-3, oakley-ec2n-4, brainpoolp160r1,
  brainpoolp160t1, brainpoolp192r1, brainpoolp192t1,
  can be brute-forced in feasible time
