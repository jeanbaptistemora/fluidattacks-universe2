---
slug: another-proud-son-json/
title: Another Proud Son of JSON
date: 2017-05-04
subtitle: Using JSON Web Token to send data
category: identity
tags: security, information, jwt
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1620330659/blog/another-proud-son-json/cover_udy9xc.webp
alt: Text editor with code highlighting
description: Here we introduce JSON Web Token, a simple, quick way
  to send secure, digital signed data from one part to another via
  URL using a base64 algorithm to encode.
keywords: JSON, Security, Digital Signature, Web Token, JWT,
  Information, Pentesting, Ethical Hacking
author: Juan Aguirre
writer: juanes
name: Juan Esteban Aguirre González
about1: Computer Engineer
about2: Netflix and hack.
figure-caption: Figure
source: https://unsplash.com/photos/OqtafYT5kTw
---

Today everything is connected, and thus, everything is communicated.
Security has become a major issue in the complex world of web
applications and their communications.

<div class="imgblock">

![jwt](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330656/blog/another-proud-son-json/image3_qksfgj.webp)

<div class="title">

Figure 1. JSON Web Token JWT

</div>

</div>

## JSON Web Token

A JSON Web Token (JWT) is a URL safe way to represent a set of
information between two parties. The information shared between the
parties can be referred to as claims. It is a safe way to transfer
information because it can be signed using a secret or using a public or
private key. The token is a base64 encoded string which due to its short
length is meant for space constrained environments.

There are two basic scenarios in which the use of a JWT is recommended.

1. Once a user is authenticated in an application and wishes to make
    subsequent requests, each one of those request should include a JWT
    to make sure that the user has access to certain routes, services or
    resources.

2. To exchange information in a secure manner making use of the
    signature. The signature is calculated based on the body and the
    payload of the JWT which allows a party to know if the message has
    been tampered with (Auth0, 2015).

<div class="imgblock">

![jwt-structure](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330658/blog/another-proud-son-json/image1_sjqdcz.webp)

<div class="title">

Figure 2. JWT Structure example - [JWT](https://jwt.io/)

</div>

</div>

The JWT is made up of three parts that are separated by a single dot.
Remember all the values are base64 encoded (header.payload.signature).

1. Header

    1. Algorithm This refers to the algorithm used to sign the token.
        Usually HMAC SHA256 or RSA.

    2. Type Refers to the type of token. In this case "JWT".

2. Payload:

    1. Claims (Names are only 3 characters long) Statements about the
        user/entity and any additional metadata. Types of claims:

        1. Reserved: Predefined but not mandatory.

        2. Public : Defined by the user. Should be defined in a
            collision resistant namespace.

        3. Private : Custom created to share information between
            parties.

3. Signature: This is made by taking the encoded header, payload and
    secret/key and using the algorithm specified in the header to sign
    it.

### How it works

<div class="imgblock">

![jwt-flow](https://res.cloudinary.com/fluid-attacks/image/upload/v1620330659/blog/another-proud-son-json/image2_hvbe9y.webp)

<div class="title">

Figure 3. JWT Flow

</div>

</div>

As we can see in the image above, we have three entities. The user, the
authentication server and the application server. Here we have four
steps.

1. Initial Authentication The user first signs in to the authentication
    server. If we are talking about a company this could be the active
    directory.

2. JWT Generation The JWT is created by the authentication server and
    sent to the user to be used in further request.

3. User Request The user then makes an API call. In a company this
    could be a query made in the company’s billing system. The JWT is
    added to the original request and sent to the application server.

4. JWT Verification The application server, billing system in our
    example, makes sure the call is coming from an authenticated user by
    checking the JWT and then returns a response to the user.

### JWT Security

Remember the data in the JWT is encoded and signed but not encrypted.
The data is encoded to transform the data structure and allow
transportation following a standard definition. The data is signed to
verify authenticity which lets me know if a message has been tampered
with but it does not prevent it.

Here is a great article on how to [Use JWT The Right
Way\!](https://stormpath.com/blog/jwt-the-right-way)

Other alternatives like SAML (Security Assertion Mark-up Language) imply
larger XML documents. JWTs are great when we have space constrained
environments and are looking to guarantee the authenticity of the data
being transported.

## References

1. [Auth0. (2015, January 1). Introduction to JSON Web Tokens.
    Retrieved May 3, 2017](https://jwt.io/introduction/)

2. [Internet Engineering Task Force IETF. (2015, May 1). RFC 7519.
    Retrieved May 3, 2017](https://tools.ietf.org/html/rfc7519)

3. [Stecky, M. (2016, May 16). 5 Easy Steps .to Understanding JSON Web
    Tokens. Retrieved May 3,
    2017](https://medium.com/vandium-software/5-easy-steps-to-understanding-json-web-tokens-jwt-1164c0adfcec)
