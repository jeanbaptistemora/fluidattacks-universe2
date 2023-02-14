---
id: libpath
title: Lib path vulnerabilities
sidebar_label: Libpath
slug: /development/products/skims/guidelines/sast/libpath
---

The following two-step procedure is used:

1. Parse a file written in the supported extensions into an iterable object
1. Search vulnerabilities by looping through the object looking for
  miss configured values or properties.

## 1. Code parsing

There are several parsing methods that have been developed overtime in order
to describe the most important characteristics of a given configuration file.
In general, files are parsed into a dictionary consisting of nodes or other
similar data structures which contain all the relevant information.

It is recommended that the developer uses similar methods within the library
to check for existing helper functions and methodologies.

## 2. Vulnerability search

The data structures result of the parsing methods are generally made up of
Nodes or Dictionaries that contain key-value pairs to describe the contents
of the file.

Thus, for most methods, the vulnerability search consists of filtering this
data structure and comparing the values of the relevant keys to any possible
vulnerable configuration, such as wildcards (*), overprivileged access or
miss configured services.
