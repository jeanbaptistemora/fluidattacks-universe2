---
id: opensearch
title: OpenSearch
sidebar_label: OpenSearch
slug: /development/stack/aws/opensearch
---

## Rationale

[OpenSearch][opensearch] is an open-source search engine forked from
[ElasticSearch][elasticsearch] that came as a response to some
[licensing issues][issues] Amazon had with Elastic, the original developers.

- It is maintained by AWS and a community of developers.
- It enables full-text search over indexed data with a flexible API.
- It is a [SaaS-oriented][saas],
  so it does not require managing infrastructure on our own.
- It supports [local deployments][local], enabling us to run it on our machines,
  which is especially useful for development and
  [ephemeral environments][ephemerals].
- All its settings can be [written as code][terraform_opensearch] using
  [Terraform][terraform].

## Alternatives

- [ElasticSearch (on AWS)][es_aws]: Not recommended as the last supported
  version before the license change is 7.10, which is quite old now.
- [ElasticSearch (on Elastic Cloud)][es_ec]: It implies using a different cloud
  provider with its own pricing model for very little extra features compared to
  what's available with OpenSearch.

## Usage

We use [OpenSearch][opensearch] for powering search and filtering features in
our [ARM Platform][arm].

## Guidelines

- You can access the [OpenSearch][opensearch] console
  after [authenticating to AWS][aws_guidelines].
- Any changes to [OpenSearch][opensearch] infrastructure
  must be done via [merge requests][mr].
- The production instance is deployed behind the [VPC][vpc], if you require
  access locally, connect using the [VPN][vpn].

[opensearch]: https://opensearch.org/
[elasticsearch]: https://www.elastic.co/elasticsearch/
[issues]: https://www.elastic.co/blog/why-license-change-aws
[saas]: https://en.wikipedia.org/wiki/Software_as_a_service
[local]: https://opensearch.org/downloads.html
[ephemerals]: /about/security/integrity/developing-integrity#ephemeral-environments
[terraform_opensearch]: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/opensearch_domain
[terraform]: /development/stack/terraform/
[es_aws]: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elasticsearch_domain
[es_ec]: https://registry.terraform.io/providers/elastic/ec/latest/docs/resources/ec_deployment
[arm]: https://fluidattacks.com/categories/arm/
[aws_guidelines]: /development/stack/aws#guidelines
[mr]: https://docs.gitlab.com/ee/user/project/merge_requests/
[vpc]: /development/stack/aws/vpc
[vpn]: /development/stack/aws/vpn#accessing-the-vpn
