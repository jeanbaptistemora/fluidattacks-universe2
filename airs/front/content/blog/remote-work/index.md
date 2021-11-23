---
slug: remote-work/
title: Always 100% Ready for Remote Work
date: 2020-04-07
subtitle: The product of a valuable effort over ten years ago
category: opinions
tags: security, company, business, protect, information, healthcare
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620331053/blog/remote-work/cover_sszd41.webp
alt: Photo by Charles Deluvio on Unsplash
description: Here is an overview of what our technological architecture
  and our way of operation are, which allow us to have the capacity
  to work 100% remotely and safely.
keywords: Remote Work, Security, Company, Business, Protect, Information,
  Healthcare, Ethical Hacking, Pentesting
author: Rafael Alvarez
writer: ralvarez
name: Rafael Alvarez
about1: Fluid Attacks co-founder and CTO
about2: Computer Engineer.
source: https://unsplash.com/photos/usxGRltb0Rk
---

Back in **2009**, `Fluid Attacks` experienced one of the most
significant cultural changes in its history: selling all its offices,
furniture and belongings, and keeping only its laptops. At that time, we
discovered the potential of the cloud. We migrated all our systems to
it. We sold our technical room, its servers, `UPS`, backup tape systems,
everything. We sold everything\!

Everyone was authorized to work from home, keeping only a new and small
office with a single workstation for administrative tasks, and a meeting
room for some face-to-face meetings.

The leading providers at that time were `Amazon` for all the
infrastructure, and `Google` for the entire collaboration suite. With
these two elements —plus a `VPN` system customized by us in the `Amazon`
infrastructure— we were able to operate fully dispersed in less than a
month, after almost eight years working a few meters away.

The first six months of this exercise were the best of that time:
productivity increased, distractions were minimized, and staff reported
comfort and happiness. Costs were minimal, even considering the remote
work allowance given to all talents for the Internet and other expenses.
The company’s flexibility to grow was high, as the purchase of a laptop
was sufficient. However, after those six months, the company was
different.

Making a company grow by home office means that communication that was
once informal now becomes formal. You stop seeing your colleagues'
faces, and the sense of urgency is not remotely conveyed. The induction
and training that used to come naturally now need to be formally
defined. And the integrations that used to emerge organically must now
be determined.

During all this time, we organized face-to-face meetings on Fridays from
**5 PM** to **6 PM**, in which we watched films, gave technical talks,
updated the company on new colleagues, carried out integration
activities in different places, etc. However, these spaces could never
achieve the closeness that sharing a physical space allows. Besides
that, what used to be an agile and fast company implementing changes
became a slow and pachydermic one.

So, we decided to return to a traditional face-to-face working mode and
buy back an office, but keeping remote work as a contingency mechanism,
either for individual exceptions or for general company eventualities.
Holding this position available, indicated to us that from the
technological point of view, the systems facilitating remote work should
remain: laptop for all, dedicated internet channels or `VPNs` with the
clients, and central systems (`IaaS` and `PaaS`) in the cloud. Besides,
an automatic time control system (`Time Doctor`) that would facilitate
the identification of moments of low productivity or low use, and a
central active directory as a service (`JumpCloud`), that would allow
the remote management of equipment that required support or backup.

In addition to all these systems, which are still in place today, the
organization and technology have been evolving and providing us with
more possibilities. In the past, we used `Yubico` tokens, which,
assigned to each employee, reinforced the security of the `VPNs`,
generated `OTP` keys with less exposure time, and also did not require a
battery. However, provisioning a token is more complicated in
non-physical environments. For this reason, today, our security scheme
is reinforced by an identity and authentication management tool such as
`Okta`. With it, all employees must enter a user before entering any
system, enter a passphrase (we do not recommend passwords), and also
confirm that they are authenticating through push notification by an
out-of-band channel (`OOB`). This must be done from their cell phones,
which, granted they have biometric devices, forces them to present
facial or fingerprint authentication. Only then they will have access to
a portal where they can enter all of the organization’s systems. From
this portal, a record is kept of who accessed what, and the
system-system keys are rotated without impacting the users.

It only remains to mention that our approach to product in the last
decade makes us operate on a system that, consistent with our
convictions, is totally in the cloud and in the most outsourced mode
possible: `Gitlab SaaS` version. For security and transparency, all our
developments are open to the public to be audited by anyone. This
implies that they are available under an `Open Source` license, which
enables us to have the most robust version: `Ultimate`. Through
`Gitlab`, we do all the version management, issues management,
configuration management, and change coordination in all our systems,
including web pages and servers.

In this sense, the current `COVID-19` pandemic has been for us nothing
more than a sad moment for humanity, for many people who are losing
their loved ones, and for others who are seeing their way of life
affected. For us, from no perspective has it represented a technological
or operational challenge. Everything has been in place for more than ten
years to operate normally in the face of this difficult time.

The office is now empty, with only chairs and large screens arranged for
the comfort and ergonomics of our absent talent. There is no
information, documents, or objects of value there, except for some
beautiful plants that harmonize and embellish the place. We have some
disquiet, though, for we do not know how we will find them when we
return.
