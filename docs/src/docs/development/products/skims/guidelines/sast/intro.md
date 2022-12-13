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

## Lib apk vulnerabilities

As the name implies, this library includes checks for vulnerabilities
in .apk files.

## Lib path vulnerabilities

This library includes checks for the most common tools that can be used to
set up Infrastructure As Code, among them, terraform, cloud formation,
Kubernetes, bash scripting and Dockerfiles.

## Lib root vulnerabilities

The methods included in the lib_root folder of the skims repo
analyze code in the following languages:

- Kotlin and Go (Not in active development at the moment)
- C#, Java, JavaScript, TypeScript and Dart (In active development)

In addition to the methods in lib_root, this library also aggregates
methods that are stored in an additional folder called sast. This is a previous
iteration of the lib_root methodology (See the specific section in the
documentation for more detail) and is currently being deprecated by
migrating the remaining methods into lib_root.

## Lib sast

This library aggregates the lib path and lib root checks to perform a
common run in the root environment of the client.

For a more detail explanation of these libraries and how to start
developing methods in each, please refer to each section in this documentation.
