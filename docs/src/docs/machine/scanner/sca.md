---
id: sca
title: SCA
sidebar_label: SCA
slug: /machine/scanner/sca
---

It is based on analyzing packages,
dependencies,
or third-party libraries used by
the application and evaluating
their security.

The package handlers supported
by each language are as follows:

| Language          | Package handler    |
|-------------------|--------------------|
| CSharp            | NuGet              |
| Dart              | Pub                |
| Go                | Go                 |
| Java              | Maven, Gradle, SBT |
| Javascript/NodeJS | NPM, Yarn          |
| PHP               | Composer           |
| Python            | pip                |
| Ruby              | Rubygems           |

With these languages, we apply the following rules:

1. Components with minimal dependencies

1. Verify third-party components
