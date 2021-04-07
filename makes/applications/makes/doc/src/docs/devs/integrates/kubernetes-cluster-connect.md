---
id: kubernetes-cluster-connect
title: Connect to Kubernetes Cluster
sidebar_label: Connect to Kubernetes Cluster
slug: /devs/integrates/kubernetes-cluster-connect
---

## Connect to cluster

In order to connect to the Integrates Kubernetes Cluster, you must:

1. Login as an Integrates developer using [this guide](/devs/integrates/get-dev-keys)
2. Install kubectl with `nix-env -i kubectl`
3. Select cluster by running `aws eks update-kubeconfig --name integrates-cluster --region us-east-1`
4. Run `kubectl get node`

Your input should be similar to this:

```
$ kubectl get node
NAME                            STATUS   ROLES    AGE   VERSION
ip-192-168-5-112.ec2.internal   Ready    <none>   58d   v1.17.9-eks-4c6976
ip-192-168-5-144.ec2.internal   Ready    <none>   39d   v1.17.11-eks-cfdc40
ip-192-168-5-170.ec2.internal   Ready    <none>   20d   v1.17.11-eks-cfdc40
ip-192-168-5-35.ec2.internal    Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-5-51.ec2.internal    Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-6-109.ec2.internal   Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-6-127.ec2.internal   Ready    <none>   18d   v1.17.11-eks-cfdc40
ip-192-168-6-135.ec2.internal   Ready    <none>   31d   v1.17.11-eks-cfdc40
ip-192-168-6-151.ec2.internal   Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-6-221.ec2.internal   Ready    <none>   13d   v1.17.11-eks-cfdc40
ip-192-168-7-151.ec2.internal   Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-7-161.ec2.internal   Ready    <none>   33d   v1.17.11-eks-cfdc40
ip-192-168-7-214.ec2.internal   Ready    <none>   61d   v1.17.9-eks-4c6976
ip-192-168-7-48.ec2.internal    Ready    <none>   30d   v1.17.11-eks-cfdc40
ip-192-168-7-54.ec2.internal    Ready    <none>   39d   v1.17.11-eks-cfdc40
```

## Common commands

These are the most commonly used kubectl commands for debugging

| Command                                                           | Example                                                                                            | Description                   |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------- |
| `kubectl get pod -A`                                              | NA                                                                                                 | Get all running pods          |
| `kubectl get node -A`                                             | NA                                                                                                 | Get all cluster nodes         |
| `kubectl describe pod -n <namespace> <pod>`                       | `kubectl describe pod -n ephemeral integrates-dsalazaratfluid-7c485cf565-w9gwg`                    | Describe pod configurations   |
| `kubectl logs -n <namespace> <pod> -c <container>`                | `kubectl logs -n ephemeral integrates-dsalazaratfluid-7c485cf565-w9gwg -c integrates1`             | Get container logs from a pod |
| `kubectl exec -it -n ephemeral <pod> -c <container> -- <command>` | `kubectl exec -it -n ephemeral integrates-dsalazaratfluid-7c485cf565-w9gwg -c integrates1 -- bash` | Access container within pod   |
