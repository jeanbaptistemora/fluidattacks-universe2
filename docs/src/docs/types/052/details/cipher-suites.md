---
id: cipher-suites
title: Cipher Suites
sidebar_label: Cipher Suites
slug: /types/052/details/cipher-suites
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

## Vulnerable bulk encryption algorithm

- [AES in ECB mode](https://www.skylinetechnologies.com/Blog/Skyline-Blog/May_2020/bye-bye-bye-to-aes-ecb-mode),
  ECB mode leaks information about the plain text
- [AES in CBC mode with padding different than 'none'](https://docs.microsoft.com/en-us/dotnet/standard/security/vulnerabilities-cbc-mode),
  Vulnerable to padding-oracle
- [Blowfish](https://en.wikipedia.org/wiki/Blowfish_(cipher)),
  Vulnerable to birthday-attacks
- [DES](https://en.wikipedia.org/wiki/Data_Encryption_Standard),
  Vulnerable to brute force attacks
- [DESede, TripleDES](https://en.wikipedia.org/wiki/Triple_DES),
  vulnerable to meet-in-the-middle attack
- [IANA and OpenSSL cipher suites](https://gitlab.com/fluidattacks/product/-/blob/59c17ec0f4ed40924ba9fc764f792dd078c0d5b1/skims/static/cryptography/cipher_suites.csv),
  Vulnerable to different kind of attacks
- [RC2](https://en.wikipedia.org/wiki/RC2),
  Vulnerable to related-key attacks using chosen plaintext
- [RC4](https://en.wikipedia.org/wiki/RC4),
  Vulnerable to bit-flipping attack and stream cipher attack
- [RSA without OAEP](https://cwe.mitre.org/data/definitions/780.html).
  Encryption is weakened without OAEP
- [SSL algorithms other than: tls, tlsv1.2, tlsv1.3, dtls, dtlsv1.2, dtlsv1.3](https://httpd.apache.org/docs/2.4/ssl/ssl_intro.html),
  Vulnerable to different kind of attacks
- Others with less adoption

## Vulnerable hashing and MAC algorithms

- [Adler](https://en.wikipedia.org/wiki/Adler-32),
  Insufficient time/space complexity
- [CRC](https://en.wikipedia.org/wiki/Cyclic_redundancy_check),
  Insufficient time/space complexity
- goodFastHash,
  Focused on speed, not security
- [MD2](https://en.wikipedia.org/wiki/MD2_(hash_function)),
  Vulnerable to pre-image and collision attacks
- [MD4](https://en.wikipedia.org/wiki/MD4),
  Vulnerable to collision attacks
- [HMACMD5, MD5, MD5Cng, MD5CryptoServiceProvider, MD5Managed](https://www.kb.cert.org/vuls/id/836068/),
  Vulnerable to collision attacks
- [HMACRIPEMD160, RIPEMD160, RIPEMD160Managed](https://en.wikipedia.org/wiki/RIPEMD),
  Insufficient time/space complexity
- [MACDES](https://en.wikipedia.org/wiki/Data_Encryption_Standard),
  Vulnerable to brute force attacks
- [MACTripleDES](https://en.wikipedia.org/wiki/Triple_DES),
  vulnerable to meet-in-the-middle attack
- [HMACSHA1, SHA1, SHA1Cng, SHA1CryptoServiceProvider, SHA1Managed](https://sslrenewals.com/blog/vulnerability-risk-in-using-sha1-certificate)
  Vulnerable to colission attacks

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
