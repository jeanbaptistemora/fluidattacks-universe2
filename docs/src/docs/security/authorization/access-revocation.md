---
id: access-revocation
title: Access revocation
sidebar_label: Access revocation
slug: /security/authorization/access-revocation
---

When employees go on vacation or leave the company, it is essential to revoke their access to the
systems and information that are accessible to them. At `Fluid Attacks`, we have a two-step
process for access revocation:

1. **Deactivating IAM account:** By doing this, users lose access to all the company applications
and client data. This includes ASM, mail, etc.

2. **Removing Git repository access:** Users can no longer see confidential information from the
repository, such as registry images, confidential issues,
[Merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/), etc.

It is worth noting that ease of access revocation is fundamental when dealing with sensitive data
in an organization; that is why we have put so much effort into making this process as simple
as possible.
