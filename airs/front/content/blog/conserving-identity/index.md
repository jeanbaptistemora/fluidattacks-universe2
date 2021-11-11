---
slug: conserving-identity/
title: Conserving Your Identity
date: 2017-05-02
category: identity
subtitle: Using WS-Security to secure  your web apps
tags: web, security, information
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330835/blog/conserving-identity/cover_cjoev1.webp
alt: Chess piece different from the others
description: In this article, we present a secure way to exchange information
  between different web services using the realms
  of the Web Service Federation (WSF).
keywords: Web Service, Security, Information, Message Exchange, Application,
  WS Federation, Ethical Hacking, Pentesting
author: Juan Aguirre
writer: juanes
name: Juan Esteban Aguirre González
about1: Computer Engineer
about2: Netflix and hack.
source: https://unsplash.com/photos/G1yhU1Ej-9A
---

In the digital era, everything is or has a web application. Web apps are
no longer just about content delivery. They have evolved to solve
complex business needs and have become a mechanism for application
integration. The communication and integration of these apps are most
commonly done through Web Services (WS), and with the growing concern
over cybersecurity comes the need to securely communicate via WS.

<div class="imgblock">

![fe-ws](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330834/blog/conserving-identity/image1_brolpf.webp)

<div class="title">

Figure 1. Federated Identity and Web Services

</div>

</div>

WS-Security defines the basic mechanism for secure message exchange.
This specification uses these base mechanisms and defines additional
primitives and extensions for security token exchange in order to enable
the issuance and dissemination of credentials within different domains.
Pretty much all it does is attach signatures, security tokens and
headers to SOAP messages. Before two parties can securely communicate,
each party needs to determine if they can "trust" the other. Trust is
understood as the expression or relationship between parties where one
of them will believe statements or claims made by another party. It is
based on evidence, history, experience, documents and more (WS-Trust
1.4, 2012). The two parties don’t have to be in the same domain to
exchange messages securely. This is where a crucial concept and the main
purpose of this article come up.

## WS-Federation

A federation is a collection of security domains, more commonly known as
realms, that have established relationships in order to securely share
resources. A Resource Provider (RP) in one realm can provide authorized
access to a resource it manages based on claims about a principal, such
as identity or other distinguishing attributes, that are asserted by an
Identity Provider in another realm. Identity is verified, and
relationships are established through the exchange of a security token.
WS-Federation builds on the WS-Trust encapsulation mechanism which
allows protocol processing to remain indifferent to the type of token
being transmitted. The main purpose of establishing a federation is to
facilitate the use of principal security attributes across trust
boundaries by establishing a federation context for that principal. A
Relying Party can then use this context to grant or deny access to a
given resource (Goodner et al., 2007).

Parties in a federation may have different policies for obtaining
services. Policies are established to set security requirements when
accessing a certain resource, hence assuring that my service or resource
is only accessible to the desired parties. In the same manner, different
services may have different policies within a party.

Organizations must establish federations. Then, the participants of the
federation must publish and exchange configuration information by which
common services and the policies for accessing them can be identified.
WS-Federation cannot happen until an organization decides to establish a
federation. This is usually done based on business or legal needs, not
technical ones.

### Key Concepts

#### Federation Metadata

Federation Metadata refers to all configuration information that allows
a party to identify common services within a federation and the
respective policies in place to access them. In web services this is
seen in the form of metadata documents that contain endpoint references,
claims and security tokens required to access them.

#### Authorization

WS-Federation defines an authorization model that allows the
implementation of any authorization service in order to provide a
security token and make decisions regarding access to available
services. Although an organization can implement any authorization
service they desire, a common model to interact with the service is
required.

### Adding more Security

Within WS-Federation, there are some concepts that allow an organization
to request additional information in order to authorize access to
advanced functionalities of a service, hence adding more security.

#### Attributes

A federation message may not always be sufficient to identify common
services. After an initial request to access a basic service is
authenticated, some organizations may request additional information in
order to grant access to advanced functionalities. In some cases, the
advanced functionalities contain sensitive information that cannot be
known to everyone. If an attacker is familiar with the process flow and
structure of other services, it will be easier to maliciously gain
access to sensitive information. Attributes are additional information
that is requested in order to authorize or deny access to a certain
service.

#### Pseudonym

Some organizations or individuals are very concerned with identity
fraud. This is a common risk in WS-Security, but Federation also
provides a concept that protects the user’s identity. If an attacker
manages to obtain everything needed to take over my identity in a
certain context or scope, and pseudonyms are not implemented, the
attacker can then use my identity to access services in another scope. A
pseudonym is an attribute that provides alternate identity and it can
provide different pseudonyms for different scopes, making it very
difficult for the attacker to gain access to a resource in one context
based on my identity from a different context. This way, if there is a
federation between multiple organizations in which a sensitive service
is published, in the case that one organization is compromised, this in
no way guarantees access to the same service in the other contexts.

WS-Federation enables parties to issue and rely on information from
other members of federations and to broker trust and attributes across
federations in a secure way maintaining individual and business privacy.
It integrates with the WS-Security model to enable secure and reliable
transactions between parties within and across federations (IBM, 2007).
WS-Federation is a very important step in defining a comprehensive Web
Services security strategy.

## References

1. Goodner, M., Hondo, M., Nadalin, A., McIntosh, M., & Schmidt, D.
    (2007, May 28). Understanding WS-Federation. Retrieved May 2, 2017,
    from [Understanding
    WS-Federation](https://msdn.microsoft.com/en-us/library/bb498017.aspx).

2. International Business Machines Corporation. (2007, April 1).
    Federation of Identities in a Web Services World. Retrieved May 2,
    2017, from [Federation of Identities in a Web Services
    World](https://msdn.microsoft.com/en-us/library/ms951235.aspx).

3. WS-Tust. (2012, April 25). OASIS Standard incorporating Approved
    Errata 01. Retrieved May 2, 2017, from
    [WS-Trust 1.4](http://docs.oasis-open.org/ws-sx/ws-trust/v1.4/ws-trust.html).
