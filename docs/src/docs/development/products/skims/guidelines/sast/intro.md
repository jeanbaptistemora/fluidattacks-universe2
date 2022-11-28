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

For the languages in active development at the moment, the code is parsed
using OS libraries, then an optimization algorithm generates a simplified
and common graph called the Syntax Graph, which is finally used to search for
vulnerabilities in the code.

Right now, the methods are able to search different kinds of vulnerabilities
in single files of code.

## Lib path vulnerabilities

This library includes generally all extension files that can be used to
set up Infrastructure As Code.
