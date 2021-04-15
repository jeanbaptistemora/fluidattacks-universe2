---
id: encryption-transit
title: Encryption in transit
sidebar_label: Encryption in transit
slug: /security/confidentiality/encryption-transit
---

All our applications and services have industry-standard
[encryption in transit](https://fluidattacks.com/products/rules/list/224/).

- The [Fluid Attacks](https://fluidattacks.com/) domain uses the latest
[TLSv1.3](https://fluidattacks.com/products/rules/list/181/) cryptographic protocol
for maximum in transit protection.

- We maintain an SSL A+ score from
[SSL Labs](https://www.ssllabs.com/ssltest/analyze.html?d=fluidattacks.com&latest).

- Digital certificates for [Fluid Attacks](https://fluidattacks.com/)
are renewed every 30 days in order to minimize leaks.

- We use the [HSTS](https://es.wikipedia.org/wiki/HTTP_Strict_Transport_Security)
policy to ensure that every connection to our domain goes through
[HTTPS](https://en.wikipedia.org/wiki/HTTPS).

- We demand all conections to support at least TLSv1.2.

- ASM’s database uses TLSv1.2 for in transit protection.

- We possess fully dedicated network channels with some of our biggest clients,
allowing us to isolate all unwanted traffic. This is especially useful for running
secure dynamic application hacking.

- For the rest of our clients, we use fully encrypted VPNs.

- [Ephemeral environments](https://fluidattacks.com/security/#EPH) always include a
digital certificate, validated with ACME protocol, and
[not self-signed](https://fluidattacks.com/products/rules/list/092/).
