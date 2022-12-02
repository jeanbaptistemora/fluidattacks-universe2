---
id: libpath
title: Lib path vulnerabilities
sidebar_label: Libpath
slug: /development/products/skims/guidelines/sast/libpath
---

The lib_path module of skims searches deterministic vulnerabilities in
infrastructure as code (IaC) software tools. This currently includes checks for
tools such as terraform, cloud formation, Kubernetes, bash scripts,
Dockerfiles, among others.

The following two-step procedure is used:

1. Parse the supported extensions files into iterable objects
1. Search the vulnerability using string methods or regex

For developers, the following sections explain in more detail this process and
the algorithms used in this module.

## 1. Code parsing

Most files use methods that have been developed over time to extract the
relevant information as an iterable object.

For each method and extension supported, different classes are defined to
be able to take advantage of OOP capabilities.

It is recommended that, before programming any new methods,
look around the code base and see if any of the existing functions in the
library already provide the functionality needed.

## 2. Vulnerability search

The iterable objects result of the parsing methods are generally made up of
Nodes or Dictionaries that contain key-value pairs to describe the contents
of the file.

Thus, for most methods, the vulnerability search consists of filtering this
data structure and comparing the values of the relevant keys to any possible
vulnerable configuration, such as wildcards (*), overprivileged access or
miss configured services.
