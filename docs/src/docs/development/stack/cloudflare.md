---
id: cloudflare
title: CloudFlare
sidebar_label: CloudFlare
slug: /development/stack/cloudflare
---

## Rationale

[CloudFlare](https://www.cloudflare.com/)
is our [Saas](https://en.wikipedia.org/wiki/Software_as_a_service)
provider for some infrastructure solutions like
[DNS](https://www.cloudflare.com/dns/),
[Rate limiting](https://www.cloudflare.com/rate-limiting/),
[Content delivery network](https://www.cloudflare.com/cdn/),
among others.
The main reasons why we chose it over other alternatives are:

1. Creating network and security solutions is very easy,
as all its components are seamlessly connected.
1. It provides highly detailed analytics regarding site traffic
in terms of both performance and security.
1. It has the
[Fastest privacy-focused DNS service](https://blog.cloudflare.com/announcing-1111/)
on the market.
1. It has easy-to-implement, auto-renewable, auto-validated
[SSL certificates](https://www.cloudflare.com/ssl/).
2. It provides a
[Web Application Firewall](https://www.cloudflare.com/lp/ppc/waf-x/)
with
[Preconfigured rules](https://www.cloudflare.com/learning/security/threats/owasp-top-10/),
[DDoS mitigation](https://www.cloudflare.com/learning/ddos/ddos-mitigation/),
[Rate limiting](https://www.cloudflare.com/en-au/rate-limiting/),
[Anti-bot capabilities](https://blog.cloudflare.com/super-bot-fight-mode/),
among others.
1. It has a
[CDN](https://www.cloudflare.com/cdn/)
with special
[routing protocols](https://www.cloudflare.com/products/argo-smart-routing/),
[HTTP/3 support](https://blog.cloudflare.com/http3-the-past-present-and-future/),
[Customizable cache TTL](https://support.cloudflare.com/hc/en-us/articles/218411427-What-does-edge-cache-expire-TTL-mean-#summary-of-page-rules-settings),
and [datacenters all over the world](https://www.cloudflare.com/network/).
Cache comes automatically configured and is customizable by just changing
its default settings.
1. It has
[Page rules](https://support.cloudflare.com/hc/en-us/articles/218411427-Understanding-and-Configuring-Cloudflare-Page-Rules-Page-Rules-Tutorial-)
that allow to easily implement
[HTTP redirections](https://developer.mozilla.org/en-US/docs/Web/HTTP/Redirections),
[Cache Rules, encryption rules](https://support.cloudflare.com/hc/en-us/articles/202775670-Customizing-Cloudflare-s-cache),
among others.

## Alternatives

The following alternatives were considered
but not chosen for the following reasons:

1. [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/):
Creating digital certificates required to also manage
[DNS](https://www.cloudflare.com/dns/)
validation records.
2. [AWS CloudFront](https://aws.amazon.com/cloudfront/):
Creating distributions was very slow.
Connecting them to a s3 bucket and maintaining such
connection was necessary.
A [Lambda](https://aws.amazon.com/lambda/)
was required in order to support accessing URL's
without having to specify `index.html` at the end.
Overall speaking, too much overhead was required
to make things work.
3. [AWS Route53](https://aws.amazon.com/route53/):
This service only does DNS,
It is not as fast or as flexible as
[CloudFlare's](https://www.cloudflare.com/).
1. [AWS Web Application Firewall](https://aws.amazon.com/waf/):
It needed to be connected to a load balancer serving
an application, it did not work for
[static sites](https://en.wikipedia.org/wiki/Static_web_page).
It is not as flexible as
[CloudFlare's](https://www.cloudflare.com/).

## Usage

We use CloudFlare for:

1. [Overall network configurations](https://gitlab.com/fluidattacks/product/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L1)
1. [DNS Records](https://gitlab.com/fluidattacks/product/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L79)
1. [HTTP Redirections](https://gitlab.com/fluidattacks/product/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L436)
1. [Managing security headers](https://gitlab.com/fluidattacks/product/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/fluidattacks.tf#L481)
1. [Managing digital certificates](https://gitlab.com/fluidattacks/product/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/certificates.tf)
1. [Managing rate limiting](https://gitlab.com/fluidattacks/product/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/makes/applications/makes/dns/src/terraform/rate_limit.tf)
2. [Managing CDN Cache](https://gitlab.com/fluidattacks/product/-/blob/46f915132f8ba81b787ad9061456f2411e2b02a9/airs/deploy/production/terraform/cache.tf)


## Guidelines

You can test or apply any
[CloudFlare](https://www.cloudflare.com/)
infrastructure by following the
[Terraform Guidelines](terraform#guidelines)
