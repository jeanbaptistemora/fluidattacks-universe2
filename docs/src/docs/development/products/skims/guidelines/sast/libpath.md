---
id: libpath
title: Lib path vulnerabilities
sidebar_label: Libpath
slug: /development/products/skims/guidelines/sast/libpath
---

The methods included in the lib_path folder of the skims repo
analyze code in the following extensions:

terraform, yaml, json, sh, Dockerfile

This library uses the following two-step procedure:

## 1. Code parsing

Since this code is generally more direct to parse, most files use methods
that have been developed over time to extract the relevant information
as an iterable object.

## 2. Vulnerability search

After each method uses a relevant parsing technique to generate the iterable
object, the vulnerabilities are generally searched using regex or
other more direct string methods.
