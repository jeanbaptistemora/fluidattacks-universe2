---
slug: multiple-credentials-begone/
title: Multiple Credentials Begone!
date: 2017-04-28
category: identity
subtitle: Security issues and solutions of SSO services
tags: security, credential, saml, standard
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330940/blog/multiple-credentials-begone/cover_ytxbj5.webp
alt: Multiple icon accounts
description: Here we explain how to use SAML, a popular SSO implementation
  standard for logging users into applications based on their sessions.
keywords: Security, SAML, Credentials, SSO, XML, Risks, Ethical Hacking,
  Pentesting
author: Juan Aguirre
writer: juanes
name: Juan Esteban Aguirre González
about1: Computer Engineer
about2: Netflix and hack.
figure-caption: Figure
source: https://unsplash.com/photos/2kH-6T6x_0I
---

The evolution of information technology brings with it many challenges,
one of the biggest ones being Identity and Access Management. To take
care of the growing vulnerabilities and attacks in this area, experts
often recommend a Single Sign-on service (SSO). One of the most popular
solutions implemented across many different industries and the focus of
this article is SAML, Security Assertion Mark-up Language.

<div class="imgblock">

![saml](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330938/blog/multiple-credentials-begone/image2_e8atbw.webp)

<div class="title">

Figure 1. Single Sign-on Services and SAML

</div>

</div>

## SAML - Security Assertion Mark-up Language

SAML is a standard for logging users into applications based on their
sessions in another context. Most organizations already know the
identity of users because they are logged in to their Active Directory
domain or Intranet. It is only logical to use this information to log
users in to other applications such as web-based application. This SSO
login standard has two main advantages over authentication with more
traditional methods like user name/password. 1. No need to type in
credentials 2. No need to remember and renew passwords (Onelogin, 2016)

<div class="imgblock">

![flow](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330938/blog/multiple-credentials-begone/image1_qyrulq.webp)

<div class="title">

Figure 2. SAML flow

</div>

</div>

SAML SSO works by transferring the user’s identity from one place, the
identity provider (IP), to another, the service provider (SP). This is
done through an exchange of digitally signed XML (eXtensible Mark-up
Language) documents. If the IP is the company’s Active Directory and the
user authenticated against the AD when he sat down to work then his
identity is already verified and known by the IP. Now if the user wants
to log in to another web application, maybe an accounting app or the
company’s ERP, once he accesses the app, this app will redirect the user
back to the IP and ask for authentication. In this case, the user is
already authenticated and there is no need to type in credential, so the
IP builds and sends the response in form of an XML document and signed
with an X.509 certificate. Once the SP validates the authentication
received in the response and it makes sure it has a valid signed
certificate then the identity of the user is established and he is
granted access to the web application (Onelogin, 2016).

## Problems and Vulnerabilities

This all works very well but one of the most common problems with this
service is misconfiguration. Failing to correctly configure your SSO
service will result in many vulnerabilities. Misconfiguration gives an
attacker the possibility of tampering with the data being exchanged. If
the attacker is able to place himself between all communications between
the service provider and the identity provider he can then intercept and
modify the SAML messages being exchanged however he sees fit.

<div class="imgblock">

![structure](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330938/blog/multiple-credentials-begone/image3_at7umz.webp)

<div class="title">

Figure 3. SAML message structure

</div>

</div>

The most common areas of SAML messages that are prone to tampering are
signatures and assertions. The signature enforces the trust relationship
between the IP and SP. The assertion instructs the SP on what trusted
operations to perform, usually to grant access to the application as a
certain user (Jensen, 2017).

## Common Attacks and Solutions

The two most commonly seen attacks in SAML are XML wrapping attacks and
replaying attacks.

### XML Wrapping

XML wrapping consist in wrapping or encapsulating a malicious payload
within a SAML message without invalidating the original message. This is
seen in SAML as XML assertion and signature wrapping, where the concept
remains the same and the payload is added as a malicious assertion or
signature. Since this doesn’t modify the original assertion’s or
signature’s body, the message will still be valid.

Remember the SAML message is just an XML document and is full of tags.
One of the tags is the signature or assertion the system needs. The
getElementsByTagName() method returns a list of all the selected XML
elements in the document. We focus on this method because it is the most
popular amongst developers, probably because of its simplicity.
.SamlConfig.Java

``` java
NodeList nodes = document.getElementsByTagName("saml:Assertion");
element = (Element) nodes.item(0);
```

Doing this, the developer is making a very dangerous assumption, that
the needed tag is the first and only tag. This assumption is what the
attacker exploits by encapsulating a malicious assertion before the
original one, hence becoming the item 0.

To solve this problem we have something called secure validation of SAML
assertions. This consist of two steps. 1. Parsing the XML document and
validating the structure based on a provided schema 2. Digital signature
validation, which verifies authenticity and integrity

The first step helps prevent wrapping. The second prevents forgery.
(Krawczyk, 2012)

### Replaying

A replaying attack consist in replaying expired messages or resending
the messages to another application. This is done with the intention of
gaining valuable information or even replaying sessions and taking
control.

SAML provides protection from replay attacks by requiring the use of SSL
encryption when transmitting assertions and messages specifically to
prevent interception of assertions. SAML also has artifacts. Artifacts
eliminate the browser from the middle of the message exchange. This way
sensitive data can be hidden from the end user or attackers between the
site and the end user. With the correct configuration the SAML source
site will only return the assertion to the requester to which the
artifact was sent.

In the end it all comes to proper configuration. To take advantage of
all the security measures that SAML has, proper and complete
configuration must be set up. It’s like taking apart a desk and when you
put it back together if you have screws leftover, you know it’s
definitely coming apart, that desk is breaking, maybe not immediately
but definitely at sometime. The same with SAML you can’t have any screws
left over when you configure the service.

## References

1. [Attacking SSO: Common SAML Vulnerabilities and Ways to Find Them.
    Retrieved April 28,
    2017](https://blog.netspi.com/attacking-sso-common-saml-vulnerabilities-ways-find/).

2. [Krawczyk, P. (2012, January 01). Secure SAML validation to prevent
    XML signature wrapping attacks. Retrieved April 28,
    2017](https://arxiv.org/ftp/arxiv/papers/1401/1401.7483.pdf).

3. [Onelogin. Dev Overview of SAML. Retrieved
    April 28, 2017](https://developers.onelogin.com/saml).
