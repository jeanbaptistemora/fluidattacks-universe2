---
id: elb
title: Elastic Load Balancing (ELB)
sidebar_label: ELB
slug: /development/stack/aws/elb
---

## Rationale

[AWS ELB][ELB] is the service we use
for exposing applications to the [Internet](https://en.wikipedia.org/wiki/Internet).
It provides load balancers using an [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
model.

The main reasons why we chose it over other alternatives are the following:

- It seamlessly integrates with
  [VPC](/development/stack/aws/vpc/),
  [EC2](/development/stack/aws/ec2/),
  [EKS](/development/stack/aws/eks/),
  etc.,
  allowing for the easy serving of applications hosted in the [cloud](https://en.wikipedia.org/wiki/Cloud_computing).
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused on granting
  that the entity follows best practices
  regarding secure cloud-based environments
  and information security.
- When combined with [Kubernetes](/development/stack/kubernetes/),
  it allows to balance application load
  by distributing requests to multiple [replicas](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
  using a [horizontal scaling approach](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
- It has its own [Kubernetes module](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
  for automatically provisioning [application load balancers][ALB]
  when Kubernetes applications are deployed.
  This is specially useful for serving [ephemeral environments](/about/security/integrity/developing-integrity#ephemeral-environments).
- It supports [VPC security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html),
  allowing us to easily set networking inbound and outbound rules
  for the load balancers.
  Such a feature is essential for avoiding [CDN bypassing](https://opendatasecurity.co.uk/how-to-bypass-cdn/).
- A single load balancer supports multiple [availability zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html),
  granting networking redundancy,
  which is essential for keeping it always available
  to the [Internet](https://en.wikipedia.org/wiki/Internet).
- It supports [health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html),
  allowing for the constant monitoring
  of all the endpoints associated to a load balancer.
  Application requests are only sent to healthy endpoints.
- [Application load balancers][ALB] support [rules](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#listener-rules),
  allowing us to create complex routing scenarios
  when it comes to request forwarding.
- It supports application load balancers,
  [network load balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html),
  and [gateway load balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html),
  providing infrastructure for a wide range of solutions.
- Load balancers can be monitored
  via [CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

> **Note:**
> [GCP Cloud Load Balancing](https://cloud.google.com/load-balancing)
> and [Azure Load Balancer](https://azure.microsoft.com/en-us/services/load-balancer/)
> are alternatives.
> A review of each of them is pending.

## Usage

We use [ELB][ELB] for

- serving our [ASM](https://fluidattacks.com/categories/asm/)
  [production environment](https://gitlab.com/fluidattacks/product/-/blob/527c74bf5984f74582a8d9620a6f9c5ae54d2838/makes/applications/integrates/back/deploy/dev/k8s/ingress.yaml#L6),
  and
- serving our ASM [ephemeral environments](https://gitlab.com/fluidattacks/product/-/blob/527c74bf5984f74582a8d9620a6f9c5ae54d2838/makes/applications/integrates/back/deploy/prod/k8s/ingress.yaml#L6).

We do not use ELB for serving [our website](https://fluidattacks.com)
and [documentation](https://docs.fluidattacks.com),
as they are static sites served by [S3](/development/stack/aws/s3/),
which directly provides [endpoints](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html)
without having to manage load balancers.

## Guidelines

- You can access the ELB console
  after [authenticating on AWS](/development/stack/aws#guidelines).
- Any changes to ELB's infrastructure must be done
  modyfing [its modules](https://gitlab.com/fluidattacks/product/-/blob/527c74bf5984f74582a8d9620a6f9c5ae54d2838/makes/applications/integrates/back/deploy/prod/k8s/ingress.yaml)
  via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).

[ELB]: https://aws.amazon.com/elasticloadbalancing/
[ALB]: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html
