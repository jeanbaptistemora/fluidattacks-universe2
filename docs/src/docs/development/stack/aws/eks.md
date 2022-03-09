---
id: eks
title: Elastic Kubernetes Service (EKS)
sidebar_label: EKS
slug: /development/stack/aws/eks
---

## Rationale

[AWS EKS][EKS] is the service we use
for hosting our [Kubernetes Cluster][KUBERNETES]
in the [cloud](https://en.wikipedia.org/wiki/Cloud_computing).
It allows us to completely manage the system
using an [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service)
approach.

The main reasons why we chose it over other alternatives are the following:

- It seamlessly integrates with other [AWS][AWS] services,
  allowing us to easily integrate with [EC2](/development/stack/aws/ec2/)
  for [automatic worker provisioning](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler),
  [IAM](/development/stack/aws/iam/)
  for [in-cluster authentication and authorization](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/variables.tf#L55),
  [Redis](/development/stack/aws/redis/)
  for [In-VPC](/development/stack/aws/vpc/) cache,
  and [Elastic Load Balancing](/development/stack/aws/elb/)
  for serving applications.
- As all its infrastructure is cloud based,
  administering it becomes a much simpler task.
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused on granting
  that the entity follows best practices
  regarding secure cloud-based environments
  and information security.
- It is supported by almost all [Kubernetes SIGs](https://github.com/kubernetes-sigs)
  utilities.
- Clusters can be [fully managed](https://gitlab.com/fluidattacks/product/-/blob/ba230133febd3325d0f5c995f638a176b89d32a2/makes/applications/makes/k8s/src/terraform/cluster.tf)
  using [Terraform][TERRAFORM].
- It is constantly updated to support new [Kubernetes versions](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html).
- It supports [OIDC](https://docs.aws.amazon.com/eks/latest/userguide/authenticate-oidc-identity-provider.html),
  allowing our Kubernetes Cluster to [perform actions](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/autoscaler.tf#L52)
  within AWS
  like [automatically creating load balancers](https://github.com/kubernetes-sigs/aws-load-balancer-controller)
  when applications are deployed.

## Alternatives

We tested [Google Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
a few years ago.
Google engineers are the creators of [Kubernetes][KUBERNETES],
and that is one of the main reasons why [GCP](https://cloud.google.com/gcp/)
offers a more complete service.
Overall,
its [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface)
offered many more insights
regarding [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/)
and [pods](https://kubernetes.io/docs/concepts/workloads/pods/).
It also supported Terraform,
configuring it was easier,
and support for new versions was faster.
The reason why we did not choose it over [EKS][EKS] was simple:
We needed it to integrate with other cloud solutions
that were already hosted on AWS.
This is a clear example of cloud dependency.

> **Note:**
> [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/overview/kubernetes-on-azure/)
> is another alternative.
> A review is pending.

## Usage

We use EKS for

- providing [networking infrastructure](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/network.tf)
  for our Kubernetes Cluster;
- [automatically deploying worker groups](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/cluster.tf#L29);
- connecting to [EC2](/development/stack/aws/ec2/)
  for [automatic worker provisioning](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler);
- connecting to [IAM](/development/stack/aws/iam/)
  for [in-cluster authentication and authorization](https://gitlab.com/fluidattacks/product/-/blob/086a0ace31819d4db76113a20f029c991d8375ce/makes/applications/makes/k8s/src/terraform/variables.tf#L55);
- connecting to [Redis](/development/stack/aws/redis/)
  for [In-VPC](/development/stack/aws/vpc/) cache.

## Guidelines

- Follow the [Kubernetes Guidelines](/development/stack/kubernetes/#guidelines)
  if you want to use the cluster.
- Any changes to [EKS][EKS] infrastructure must be done via
  [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- To learn how to test and apply infrastructure via [Terraform][TERRAFORM],
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).

[AWS]: /development/stack/aws/
[EKS]: https://aws.amazon.com/eks/
[KUBERNETES]: /development/stack/kubernetes/
[TERRAFORM]: /development/stack/terraform/
