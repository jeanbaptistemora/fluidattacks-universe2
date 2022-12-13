---
id: dast
title: DAST Vulnerabilities
sidebar_label: DAST
slug: /development/products/skims/guidelines/dast
---

DAST refers to "Dinamic Application Security Testing", and it is performed
by searching vulnerabilities in dynamic environments such as url endpoints and
servers.

Methods are divided between several libraries, depending on what is being
checked on the environment.

## Lib http vulnerabilities

This library checks environments and endpoints that host our clients
applications and reviews vulnerabilities in the http responses,
such as missing or miss configured headers.

## Lib ssl vulnerabilities

This library checks environments for vulnerabilities related to
connections, handshakes and other server-related checks.
