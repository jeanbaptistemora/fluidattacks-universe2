---
id: cluster
title: Cluster
sidebar_label: Cluster
slug: /development/common/cluster
---

## Architecture

1. We have one [Kubernetes cluster](/development/stack/kubernetes)
   that is shared by all the products.
1. The cluster is hosted by
   [EKS by Amazon Web Services (AWS)](/development/stack/aws/eks).
1. The cluster is divided into namespaces,
   which keep resources in isolation from other namespaces.
   - The `default` namespace is unused,
     we try to put things into a namespace appropriate to the product.
   - The `dev` namespace
     currently holds the ephemeral environments of Integrates.
   - The `prod-integrates` namespace holds the production deployment
     of Integrates,
     and a Celery jobs server.
   - The `kube-system` namespace holds cluster-wide deployments
     for New Relic, DNS, the load balancer, and the auto-scaler,
   - Other `kube-*` namespaces exist,
     but they are not used for anything at the moment.
1. Every namespace runs in a specific worker group
   whose physical machine instances run
   on [EC2 by Amazon Web Services (AWS)](/development/stack/aws/ec2).
1. The cluster spawns machine instances
   on many subnets (prefixed with `k8s_`)
   in different availability zones.

:::tip
You can right click on the image below
to open it in a new tab,
or save it to your computer.
:::

![Architecture of Common's /cluster](./common-cluster-arch.dot.svg)
