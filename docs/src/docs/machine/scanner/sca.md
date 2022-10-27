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

| Language   | Package handler    |
|------------|--------------------|
| Python     | pip                |
| Javascript | NPM, Yarn          |
| Java       | Maven, Gradle, SBT |
| CSharp     | NuGet              |
| Go         | Go                 |
| Ruby       | Rubygems           |

With these languages, we apply the following rules:

1. Components with minimal dependencies

1. Verify third-party components
