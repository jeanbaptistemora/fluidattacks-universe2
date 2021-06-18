---
id: eks
title: Elastic Kubernetes Service (EKS)
sidebar_label: EKS
slug: /development/stack/aws/eks
---

## Rationale

[AWS EKS][EKS] is the service we use
for hosting our [Kubernetes cluster][KUBERNETES]
in the
[cloud](https://en.wikipedia.org/wiki/Cloud_computing).
It allows us to completely manage the system
using a [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
approach.

The main reasons why we chose it
over other alternatives are:

1. It seamlessly integrates with other [AWS][AWS] services,
    allowing us to easily
    integrate with
    [EC2](/development/stack/aws/ec2/) for
    [automatic worker provisioning](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler),
    [IAM](/development/stack/aws/iam) for
    [in-cluster authentication and authorization](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/variables.tf#L55),
    [Redis](https://aws.amazon.com/redis/) for
    [In-VPC](https://aws.amazon.com/vpc/) cache,
    and [Elastic Load Balancing](https://aws.amazon.com/elasticloadbalancing/)
    for serving applications.
1. As all its infrastructure is
    [cloud](https://en.wikipedia.org/wiki/Cloud_computing) based,
    administering it becomes a much simpler task.
1. It is supported by almost all
    [Kubernetes SIGs](https://github.com/kubernetes-sigs)
    utilities.
1. Clusters can be
    [fully managed](https://gitlab.com/fluidattacks/product/-/blob/ba230133febd3325d0f5c995f638a176b89d32a2/makes/applications/makes/k8s/src/terraform/cluster.tf)
    using [Terraform][TERRAFORM].
1. It is constantly updated to support new
    [Kubernetes versions](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html).
1. It supports [OIDC](https://docs.aws.amazon.com/eks/latest/userguide/authenticate-oidc-identity-provider.html),
    allowing our [Kubernetes cluster][KUBERNETES]
    to [perform actions](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/autoscaler.tf#L52)
    within [AWS][AWS] like
    [automatically creating load balancers](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
    when applications are deployed.

## Alternatives

1. [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine):
    We tested it a few years ago.
    Google engineers are the creators of [Kubernetes][KUBERNETES],
    and that is one of the main reasons why [GCP](https://cloud.google.com/gcp/)
    offers a more complete service.
    Overall speaking,
    its [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)
    offered a lot more insights regarding
    [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) and
    [pods](https://kubernetes.io/docs/concepts/workloads/pods/),
    It also supported [Terraform][TERRAFORM],
    Configuring it was easier,
    and support for new versions was faster.
    The reason why we did not chose it was simple:
    We needed it to integrate with other cloud solutions
    that were already hosted in [AWS][AWS].
    This is a clear example of cloud dependency.
1. [Azure Kubernetes Service (EKS)](https://azure.microsoft.com/en-us/overview/kubernetes-on-azure/):
    Pending to review.

## Usage

We use [EKS][EKS] for:

1. Providing [Networking infrastructure](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/network.tf)
    for our [Kubernetes cluster][KUBERNETES].
1. [Automatically deploying worker groups](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/cluster.tf#L29).
1. Connecting to [IAM](/development/stack/aws/iam) for
    [in-cluster authentication and authorization](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/variables.tf#L55).
1. Connecting to [EC2](/development/stack/aws/ec2/) for
    [automatic worker provisioning](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler).
1. Connecting to [Redis](https://aws.amazon.com/redis/) for
    [In-VPC](https://aws.amazon.com/vpc/) cache.

## Guidelines

1. Follow the [Kubernetes Guidelines](/development/stack/kubernetes/#guidelines)
    if you want to use the cluster.
1. Any changes to
    [EKS][EKS]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. To learn how to test and apply infrastructure via [Terraform][TERRAFORM],
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).

[AWS]: https://aws.amazon.com/
[EKS]: https://aws.amazon.com/eks/
[KUBERNETES]: /development/stack/kubernetes/
[TERRAFORM]: /development/stack/terraform/
