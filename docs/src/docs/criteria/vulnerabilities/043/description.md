---
id: description
title: Insecure or Unset HTTP Headers
sidebar_label: Description
slug: /criteria/vulnerabilities/043
---

The server lacks security headers or defines insecure values for them.
These headers are necessary to prevent common attacks
such as XSS, Clickjacking among others.

## Recommendation

For application servers,
the required HTTP headers are the following:

- [Cache-Control](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.http/?highlight=fluidasserts%20proto%20http%20is_header_cache_control_missing#fluidasserts.proto.http.is_header_cache_control_missing)

- [Content-Security-Policy](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.http/?highlight=fluidasserts%20proto%20http%20is_header_content_security_policy_missing#fluidasserts.proto.http.is_header_content_security_policy_missing)

- [Content-Type](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.http/?highlight=fluidasserts%20proto%20http%20is_header_content_type_missing#fluidasserts.proto.http.is_header_content_type_missing)

- [Strict-Transport-Security (*HSTS*)](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.http/?highlight=fluidasserts%20proto%20http%20is_header_hsts_missing#fluidasserts.proto.http.is_header_hsts_missing)

- [X-Permitted-Cross-Domain-Policies](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.http/?highlight=fluidasserts%20proto%20http%20is_header_perm_cross_dom_pol_missing#fluidasserts.proto.http.is_header_perm_cross_dom_pol_missing)

- [X-Content-Type-Options](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.http/?highlight=fluidasserts%20proto%20http%20is_header_x_content_type_options_missing#fluidasserts.proto.http.is_header_x_content_type_options_missing)

For API servers,
the required HTTP headers are the following:

- [Content-Type](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.rest/?highlight=fluidasserts%20proto%20rest%20is_header_content_type_missing#fluidasserts.proto.rest.is_header_content_type_missing)

- [Accept](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.rest/?highlight=fluidasserts%20proto%20rest%20accepts_insecure_accept_header#fluidasserts.proto.rest.accepts_insecure_accept_header)

- [Strict-Transport-Security (*HSTS*)](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.rest/?highlight=fluidasserts%20proto%20rest%20is_header_hsts_missing#fluidasserts.proto.rest.is_header_hsts_missing)

- [X-Content-Type-Options](https://fluidattacks.gitlab.io/asserts/fluidasserts.proto.rest/?highlight=fluidasserts%20proto%20rest%20is_header_x_content_type_options_missing#fluidasserts.proto.rest.is_header_x_content_type_options_missing)

## Requirements

- [062. Define standard configurations](/criteria/requirements/062)

- [175. Protect pages from clickjacking](/criteria/requirements/175)
