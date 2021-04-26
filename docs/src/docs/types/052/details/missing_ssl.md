---
id: missing_ssl
title: Missing SSL
sidebar_label: Missing SSL
slug: /types/052/details/missing_ssl
---

SSL (Secure Sockets Layer) and its successor, TLS (Transport Layer Security),
are protocols for establishing authenticated and encrypted links between
networked computers.

The most common and well-known use of SSL/TLS is secure web browsing via the
HTTPS protocol.
Users visiting an HTTPS website can be assured of:

- **Authenticity**,
  The server presenting the certificate is in possession of the private key
  that matches the public key in the certificate.

- **Integrity**,
  Documents signed by the certificate (e.g. web pages) have not been altered in
  transit by a man in the middle.

- **Encryption**,
  Communications between the client and server are encrypted.

Because of these properties, SSL/TLS and HTTPS allow users to securely
transmit confidential information such as credit card numbers,
social security numbers, and login credentials over the internet,
and be sure that the website they are sending them to is authentic.

With an insecure HTTP website, these data are sent as plain text,
readily available to any eavesdropper with access to the data stream.
Furthermore,
users of these unprotected websites have no trusted third-party assurance that
the website they are visiting is what it claims to be.
