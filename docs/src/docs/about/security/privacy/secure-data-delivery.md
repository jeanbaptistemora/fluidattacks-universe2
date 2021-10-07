---
id: secure-data-delivery
title: Secure Delivery of Sensitive Data
sidebar_label: Secure Delivery of Sensitive Data
slug: /about/security/privacy/secure-data-delivery
---

Here is what we do
to reduce information leakage
when delivering data to our clients.

## Secure information-sharing system

We use an information-sharing system
with [DLP](https://en.wikipedia.org/wiki/Data_loss_prevention_software)
(data loss prevention)
when sending sensitive information
to our clients.
This includes contracts,
portfolios,
and other sensitive documents.

## Signed URLs

[Attack Surface Manager (ASM)](https://app.fluidattacks.com/)
can create signed download URLs
with an expiration date
when downloading reports,
meaning that links expire
and can only be used by the user
who requested the download.

## Onion routing

The [`Fluid Attacks` domain](https://fluidattacks.com/)
supports [Onion routing](https://en.wikipedia.org/wiki/Onion_routing),
which enhances user privacy
and enables more fine-grained protection.

## Passphrase-protected reports

All reports downloaded via ASM
have a randomly generated four-word passphrase.
This passphrase is sent to the email of the user
who requested the download.
This applies to both XLS and PDF formats.

## Watermarked reports

Every report downloaded via ASM comes with a watermark
on all its pages,
specifying that only the individual who generated it
is allowed to read it.
This is used as a measure to identify
who generated the report in the first place
and discourage its distribution
through channels other than [ASM](https://app.fluidattacks.com/).
