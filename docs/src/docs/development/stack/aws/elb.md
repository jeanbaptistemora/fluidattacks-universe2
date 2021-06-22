---
id: elb
title: Elastic Load Balancing (ELB)
sidebar_label: ELB
slug: /development/stack/aws/elb
---

## Rationale

[Elastic Load Balancing][ELB]
is the [AWS](/development/stack/aws/) service
we use for exposing
applications to
[Internet](https://en.wikipedia.org/wiki/Internet).
It provides load balancers using a
[IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
model.

The main reasons why we chose it
over other alternatives are:

1. It seamlessly integrates with
    [VPC](/development/stack/aws/vpc/),
    [EC2](/development/stack/aws/ec2/),
    [EKS](/development/stack/aws/eks/),
    etc.
    Allowing to easily serve
    applications hosted in the
    [cloud](https://en.wikipedia.org/wiki/Cloud_computing).
1. When combined with
    [Kubernetes](/development/stack/kubernetes/),
    it allows to balance application load
    by distributing requests to multiple
    [replicas](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
    using a
    [horizontal scaling approach](https://www.section.io/blog/scaling-horizontally-vs-vertically/).
1. It has its own
    [Kubernetes module](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
    for automatically provisioning
    [application load balancers][ALB]
    when [Kubernetes](/development/stack/kubernetes/) applications
    are deployed.
    This is specially useful for serving
    [ephemeral environments](/about/security/integrity/developing-integrity#ephemeral-environments).
1. It supports
    [VPC security groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-security-groups.html),
    allowing to easily set
    networking inbound and outbound rules
    for the load balancers.
    Such feature is essential
    for avoiding
    [CDN bypassing](https://opendatasecurity.co.uk/how-to-bypass-cdn/).
1. A single load balancer supports multiple
    [Availability zones](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html),
    granting networking redundancy,
    which is essential
    for keeping it always
    available to the
    [Internet](https://en.wikipedia.org/wiki/Internet).
1. It supports
    [health checks](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html),
    allowing to constantly monitor
    all the endpoints
    associated to a load balancer.
    Application requests are only
    sent to healthy endpoints.
1. [Application load balancers][ALB] support
    [rules](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#listener-rules),
    allowing to create
    complex routing scenarios
    when it comes to request forwarding.
1. It supports
    [application load balancers][ALB],
    [network load balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html),
    and
    [gateway load balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html),
    providing infrastructure
    for a wide range of solutions.
1. Load balancers
    can be monitored via
    [CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

1. [GCP Cloud Load Balancing](https://cloud.google.com/load-balancing):
    Pending to review.
1. [Azure Load Balancer](https://azure.microsoft.com/en-us/services/load-balancer/):
    Pending to review.

## Usage

We use [ELB][ELB] for:

1. Serving our
    [ASM](https://fluidattacks.com/categories/asm/)
    production
    [environment](https://gitlab.com/fluidattacks/product/-/blob/527c74bf5984f74582a8d9620a6f9c5ae54d2838/makes/applications/integrates/back/deploy/dev/k8s/ingress.yaml#L6).
1. Serving our
    [ASM](https://fluidattacks.com/categories/asm/)
    ephemeral
    [environments](https://gitlab.com/fluidattacks/product/-/blob/527c74bf5984f74582a8d9620a6f9c5ae54d2838/makes/applications/integrates/back/deploy/prod/k8s/ingress.yaml#L6).

We do not use [ELB][ELB] for:

Serving [our website](https://fluidattacks.com)
and [documentation](https://docs.fluidattacks.com),
as they are static sites
served by [S3](/development/stack/aws/s3/),
which directly provides
[endpoints](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteEndpoints.html)
without having to manage load balancers.

## Guidelines

1. You can access the
    [ELB][ELB] console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [ELB's][ELB]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
    by modyfing
    [its modules](https://gitlab.com/fluidattacks/product/-/blob/527c74bf5984f74582a8d9620a6f9c5ae54d2838/makes/applications/integrates/back/deploy/prod/k8s/ingress.yaml).

[ELB]: https://aws.amazon.com/elasticloadbalancing/
[ALB]: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html
