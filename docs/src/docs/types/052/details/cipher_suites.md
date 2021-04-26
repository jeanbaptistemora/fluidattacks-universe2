---
id: cipher_suites
title: Cipher Suites
sidebar_label: Cipher Suites
slug: /types/052/details/cipher_suites
---

A cipher suite is a set of algorithms that help secure a network connection.
Suites typically use Transport Layer Security (TLS) or its now-deprecated predecessor Secure Socket Layer (SSL).
The set of algorithms that cipher suites usually contain include:
a key exchange algorithm, a bulk encryption algorithm,
and a message authentication code (MAC) algorithm.

The **key exchange algorithm** is used to exchange a key between two devices.
This key is used to encrypt and decrypt the messages being sent between two
machines.

The **bulk encryption algorithm** is used to encrypt the data being sent.

The **MAC algorithm** provides data integrity checks to ensure that the data
sent does not change in transit.
In addition,
cipher suites can include signatures and an authentication algorithm to help
authenticate the server and or client.

A cipher suite is as secure as the algorithms that it contains.
If the version of encryption or authentication algorithm in a cipher suite have
known vulnerabilities the cipher suite and TLS connection is then vulnerable.

## Vulnerable cipher suites

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
