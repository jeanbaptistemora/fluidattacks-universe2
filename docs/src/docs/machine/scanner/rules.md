---
id: rules
title: Rules and Languages of Machine
sidebar_label: Rules
slug: /machine/scanner/rules
---

Machine is an automatic tool
that seeks to find vulnerabilities
in an application,
performing tests
such as SAST,
DAST,
SCA,
and auditing infrastructure
in the cloud (CLOUD).
These validation tests are
implemented for each of the
different supported languages.
They are created based on the
rules of our security criteria
([https://docs.fluidattacks.com/criteria/](https://docs.fluidattacks.com/criteria/)),
automating only the detection
of deterministic vulnerabilities
to minimize the false positive rate.

## Types of tests

### SAST

Security tests are based on
analyzing the source code
from the repositories.
The currently supported
languages and the rules
checked in each one are:

#### .net

The rules that apply are:

- Avoid disclosing technical information
- Disable debugging events
- Disable insecure functionalities
- Restrict system objects

#### Android configuration files

The rules that apply are:

- Avoid client-side control enforcement
- Avoid disclosing technical information
- Define users with privileges
- Disable debugging events
- Disable insecure functionalities
- Encrypt sensitive information
- Request authentication
- Restrict system objects
- Set user's required privileges
- Use the principle of least privilege

#### CloudFormation (Cloud)

The rules that apply are:

- Allow access only
  to the necessary ports
- Avoid client-side
  control enforcement
- Define users with privileges
- Disable insecure TLS versions
- Disable insecure
  functionalities
- Display access notification
- Encrypt sensitive
  information
- Limit password lifespan
- Mask sensitive data
- Passphrases with
  at least 4 words
- Passwords with at
  least 20 characters
- Passwords with random salt
- Prevent log modification
- Prevent the use
  of breached passwords
- Record exact occurrence
  time of events
- Record exceptional
  events in logs
- Register severity level
- Request access credentials
- Request authentication
- Restrict access to
  critical processes
- Restrict system objects
- Separate keys for
  encryption and signatures
- Set minimum OTP length
- Set minimum size
  for hash functions
- Set minimum size
  of asymmetric encryption
- Set minimum size of
  symmetric encryption
- Set user's required privileges
- Store logs based
  on valid regulation
- Store passwords with salt
- Transmit data using
  secure protocols
- Use of log management system
- Use pre-existent mechanisms
- Use secure cryptographic mechanisms
- Use the principle of least privilege

#### Configuration files (config, json, properties, settings)

The rules that apply are:

- Change system
  default credentials
- Disable insecure
  functionalities
- Make authentication
  options equally secure
- Protect system cryptographic keys
- Request authentication
- Restrict access
  to critical processes
- Source code without
  sensitive information

#### CSharp

The rules that apply are:

- Avoid client-side
  control enforcement
- Avoid deserializing
  untrusted data
- Avoid disclosing
  technical information
- Avoid session ID leakages
- Compare file
  format and extension
- Control redirects
- Cookies with
  security attributes
- Define standard configurations
- Define users with privileges
- Disable insecure TLS versions
- Disable insecure functionalities
- Discard unsafe inputs
- Include HTTP security headers
- Limit password lifespan
- Parameters without
  sensitive data
- Passphrases with
  at least 4 words
- Passwords with at
  least 20 characters
- Prevent log modification
- Prevent the use
  of breached passwords
- Restrict access
  to critical processes
- Restrict system objects
- Scan files for malicious code
- Set a rate limit
- Set maximum response time
- Set minimum OTP length
- Set minimum size
  for hash functions
- Set minimum size of
  asymmetric encryption
- Set minimum size of
  symmetric encryption
- Set user's required privileges
- Transmit data using
  secure protocols
- Use a secure programming
  language
- Use parameterized queries
- Use the principle
  of least privilege
- Validate request parameters
- Verify third-party components

#### Docker

The rules that apply are:

- Define users with privileges
- Disable insecure functionalities
- Protect system cryptographic keys
- Set user's required privileges
- Source code without sensitive information
- Use the principle of least privilege

#### Go

The rules that apply are:

- Disable insecure TLS versions
- Set minimum size for hash functions
- Set minimum size of asymmetric encryption
- Set minimum size of symmetric encryption
- Transmit data using secure protocols

#### Html

The rules that apply are:

- Avoid caching and temporary files
- Control redirects
- Discard unsafe inputs
- Use digital signatures
- Verify Subresource Integrity
- Verify third-party components

#### Java

The rules that apply are:

- Avoid client-side control enforcement
- Avoid disclosing technical information
- Cookies with security attributes
- Define users with privileges
- Disable insecure TLS versions
- Disable insecure functionalities
- Discard unsafe inputs
- Prevent log modification
- Protect system cryptographic keys
- Restrict access to critical processes
- Restrict system objects
- Set minimum size for hash functions
- Set minimum size of asymmetric encryption
- Set minimum size of symmetric encryption
- Set user's required privileges
- Source code without sensitive information
- Transmit data using secure protocols
- Uniform distribution in random numbers
- Use parameterized queries
- Use secure cryptographic mechanisms
- Use the principle of least privilege
- Validate request parameters

#### Javascript

The rules that apply are:

- Avoid caching and temporary files
- Avoid disclosing technical information
- Disable insecure TLS versions
- Disable insecure functionalities
- Keep client-side storage without sensitive data
- Protect system cryptographic keys
- Restrict system objects
- Set minimum size for hash functions
- Set minimum size of asymmetric encryption
- Set minimum size of symmetric encryption
- Source code without sensitive information
- Transmit data using secure protocols
- Uniform distribution in random numbers
- Use secure cryptographic mechanisms

#### Kotlin

The rules that apply are:

- Disable insecure TLS versions
- Set minimum size for hash functions
- Set minimum size of asymmetric encryption
- Set minimum size of symmetric encryption
- Transmit data using secure protocols

#### Kubernetes

The rules that apply are:

- Define users with privileges
- Set user's required privileges
- Use the principle of least privilege

#### Python

The rule that applies is:

- Declare dependencies explicitly

#### Terraform (Cloud)

The rules that apply are:

- Allow access only to the necessary ports
- Authenticate using standard protocols
- Avoid client-side control enforcement
- Avoid object reutilization
- Define OTP lifespan
- Define credential interface
- Define lifespan for temporary passwords
- Define users with privileges
- Disable insecure TLS versions
- Disable insecure functionalities
- Display access notification
- Encrypt sensitive information
- Exclude unverifiable files
- Implement a biometric verification component
- Limit password lifespan
- Make authentication options equally secure
- Mask sensitive data
- Passwords with random salt
- Prevent log modification
- Record exact occurrence time of events
- Record exceptional events in logs
- Register severity level
- Request access credentials
- Request authentication
- Restrict access to critical processes
- Restrict system objects
- Set minimum size for hash functions
- Set minimum size of asymmetric encryption
- Set minimum size of symmetric encryption
- Set user's required privileges
- Store logs based on valid regulation
- Store passwords with salt
- Transmit data using secure protocols
- Use of log management system
- Use the principle of least privilege

### DAST

Security testing based on
deployed functional environments.
The contexts currently
supported in DAST are:

#### HTTP

Checks on the responses that
a server gives to a request.
The rules that apply are:

- Avoid object reutilization.
- Authenticate using standard protocols
- Make authentication options equally secure
- Discard unsafe inputs
- Control redirects
- Encrypt client-side session information
- Define standard configurations
- Do not interpret HTML code
- Protect pages from clickjacking
- Include HTTP security headers
- Record exceptional events in logs
- Avoid client-side control enforcement
- Use digital signatures
- Verify third-party components
- Verify Subresource Integrity
- Cookies with security attributes

#### SSL

Checks on the encryption schemes
used in the communication.
The rules that apply are:

- Set minimum size of asymmetric encryption
- Set minimum size of symmetric encryption
- Set minimum size for hash functions
- Transmit data using secure protocols
- Disable insecure TLS versions

### SCA

It is based on
analyzing packages,
dependencies,
or third-party libraries used
by the application and
evaluating their security.

#### CSharp, Java, Javascript, Python

The rules that apply are:

- Components with minimal dependencies
- Verify third-party components

### Cloud Infrastructure

Security audit of resources
deployed in the cloud.

#### AWS

Verifications on the infrastructure
deployed in the Amazon cloud
using credentials provided
by the customer.
The rule that applies is:

- Allow access only
  to the necessary ports
