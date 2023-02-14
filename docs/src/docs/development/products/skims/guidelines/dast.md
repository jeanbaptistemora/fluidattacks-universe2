---
id: dast
title: DAST Vulnerabilities
sidebar_label: DAST
slug: /development/products/skims/guidelines/dast
---

DAST refers to "Dynamic Application Security Testing", and it is performed
by searching vulnerabilities in dynamic environments such as url end points and
servers.

Currently, the following three libraries have active methods

## LIB HTTP

This library checks environments and endpoints that host our clients
applications and reviews vulnerabilities in the http responses,
such as missing or miss configured headers.

## LIB SSL

This library checks environments for vulnerabilities related to
connections, handshakes and other server-related checks.

## LIB DAST

This library checks cloud environments safely scanning the configuration
of the client.

Currently, only AWS configurations have methods, which check
vulnerabilities in the client infrastructure using the boto3 library.
