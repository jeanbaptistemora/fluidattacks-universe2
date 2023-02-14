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

## LIB SAST

This library has methods to check for vulnerabilities in code. Overall,
it is divided in two sub libraries, lib root and lib path.

On the one hand, lib root uses graph algorithms to parse and analyze
complex code files, whereas lib_path includes languages and extensions
used for configuration and IaC.

### Lib root

The methods in this library use graph algorithms to search vulnerabilities in
complex code written in the following languages:

- C#
- Java
- JavaScript
- TypeScript
- Dart
- Kotlin
- Go
- Python (In development, not yet functional)

### Lib path

The methods in this library perform vulnerability analysis by parsing a file
into iterable objects and performing search algorithms. This is specially
useful in configuration files that do not use complex control structures or
variable definitions.

Among the languages/extensions supported are:

- Terraform (Currently being migrated to lib_root)
- Cloudformation (.yaml)
- Kubernetes
- Bash scripts
- Dockerfiles
- Config files such as .xml, .jmx, .config

## LIB APK

As the name implies, this library checks vulnerabilities by reversing
Android APK files.
