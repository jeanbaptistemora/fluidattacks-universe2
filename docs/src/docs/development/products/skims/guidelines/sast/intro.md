---
id: intro
title: SAST Vulnerabilities
sidebar_label: Introduction
slug: /development/products/skims/guidelines/sast/intro
---

SAST refers to "Static Application Security Testing", and it is performed
by searching for deterministic vulnerabilities in code files.

Methods are divided between several libraries, depending on the language
in which the code is written.

## Lib root vulnerabilities

The methods included in the lib_root folder of the skims repo
analyze code in the following languages:

- Kotlin and Go (Not in active development at the moment)
- C#, Java, JavaScript, TypeScript and Dart (In active development)

## Lib path vulnerabilities

This library includes checks for the most common tools that can be used to
set up Infrastructure As Code, among them, terraform, cloud formation,
Kubernetes, bash scripting and Dockerfiles.

## Lib http vulnerabilities

This library checks environments and endpoints that host client applications
and reviews vulnerabilities in the http responses, such as missing or
miss configured headers.

## Lib ssl vulnerabilities

This library checks environments for vulnerabilities related to
connections, handshakes and other server-related checks.

For a more detail explanation of each library and its methods, refer to each
section in this documentation.
