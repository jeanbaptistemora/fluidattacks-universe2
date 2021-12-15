---
id: ebs
title: Elastic Block Store (EBS)
sidebar_label: EBS
slug: /development/stack/aws/ebs
---

## Rationale

[AWS EBS][EBS] is the service
we use for [block-level storage](https://en.wikipedia.org/wiki/Block-level_storage).
It allows us to have [hard drives](https://en.wikipedia.org/wiki/Device_file#BLOCKDEV)
in the [cloud](https://en.wikipedia.org/wiki/Cloud_computing).
The main reasons why we chose it
over other alternatives
are the following:

- It seamlessly integrates with [AWS EC2](/development/stack/aws/ec2),
  allowing us to connect external hard drives to instances.
- It complies with [several](https://aws.amazon.com/compliance/iso-certified/)
  certifications from [ISO](https://en.wikipedia.org/wiki/International_Organization_for_Standardization)
  and [CSA](https://en.wikipedia.org/wiki/Cloud_Security_Alliance).
  Many of these certifications are focused
  on granting that the entity follows best practices
  regarding secure [cloud-based](https://en.wikipedia.org/wiki/Cloud_computing)
  environments
  and information security.
- It provides a wide range of [disk types](https://aws.amazon.com/ebs/features/#Amazon_EBS_volume_types)
  that goes from [SSDs](https://en.wikipedia.org/wiki/Solid-state_drive)
  with a size of 64 [TiB](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units)
  and a throughput of 4000 [MiB/s](https://en.wikipedia.org/wiki/Data-rate_units#Megabyte_per_second)
  to [HHDs](https://en.wikipedia.org/wiki/Hard_disk_drive)
  with a size of 16 TiB
  and a throughput of 500 MiB/s.
- It provides disks with [different specializations][GP2].
  There are General Purpose and Provisioned IOPS SSDs
  and
  Throughput Optimized and Cold HHDs.
  By having all these different types of disks,
  we can easily select which one to work with,
  depending on the nature of the problem
  we are trying to solve.
- It supports [point-in-time snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
  designed to back up all data
  that exists within a disk.
- Disks can be easily [attached](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-attaching-volume.html)
  and [detached](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-detaching-volume.html)
  from AWS EC2 machines,
  allowing us to easily change general machine configurations
  without losing any data.
- Disks can be [encrypted](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)
  using [AWS KMS](https://aws.amazon.com/kms/) keys,
  which allows encryption of data
  moving between the disk and the instance using it,
  data at rest inside the volume,
  disk snapshots,
  and all volumes created from these snapshots.
- It supports [data lifecycle policies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-lifecycle.html),
  allowing us to create, retain and delete
  disks based on created policies.
- It supports [monitoring and metrics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using_cloudwatch_ebs.html)
  using [AWS CloudWatch](/development/stack/aws/cloudwatch/).

## Alternatives

- **[Google Compute Engine (GCE)](https://cloud.google.com/compute):**
  It did not exist at the time we migrated to the cloud.
  [GCP](https://cloud.google.com/gcp) does not offer
  an equivalent to EBS.
  Instead,
  their entire [disk service](https://cloud.google.com/compute/docs/disks)
  exists within GCE.
  It does not support disk encryption.
- **[Azure Disk Storage](https://azure.microsoft.com/en-us/services/storage/disks/):**
  It did not exist at the time we migrated to the cloud
  (pending review).

## Usage

We use [AWS EBS][EBS] for

- [Gitlab CI](/development/stack/gitlab-ci) bastion
  (we use a 16 GiB [GP2][GP2] disk,
  as it only needs to have basic software installed
  such as [Gitlab Runner](https://docs.gitlab.com/runner/install/)
  and [Docker Machine](https://docs.docker.com/machine/install-machine/);
  high disk throughput is not required),
- [Gitlab CI workers](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/makes/ci/src/config.toml#L57)
  (we use 10 GiB [GP3][GP2] disks
  just for hosting our workers' [operating system][OS].
  Additionally,
  workers come with high throughput
  [50 GiB internal NVMe disks](https://aws.amazon.com/blogs/aws/ec2-instance-update-c5-instances-with-local-nvme-storage-c5d/),
  which are very useful
  for achieving as-fast-as-possible
  job performance within our [CI](/development/stack/gitlab-ci)),
- [Batch](/development/stack/aws/batch/) processing
  [workers](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/makes/compute/src/terraform/aws_batch.tf#L112)
  (we use 8 GiB GP2 disks
  just for hosting the operating system.
  These workers also come with 50 GiB internal NVMe disks),
- [Kubernetes](/development/stack/kubernetes) cluster
  [workers](https://gitlab.com/fluidattacks/product/-/blob/53879d903b3c8c2561d45552cbc53f2350601e38/makes/applications/makes/k8s/src/terraform/cluster.tf#L40)
  (we use 50 GiB GP2 disks
  for hosting the base operating system
  and stored containers
  for applications like our [ASM](https://fluidattacks.com/categories/asm/).
  High disk throughput is not required
  as our ASM does not store any data
  within local disks),
- [Okta RADIUS Agent](/development/stack/okta#usage)
  (we use a 50 GiB GP2 disk.
  It is probably oversized
  since only the base operating system
  and [RADIUS agent](https://help.okta.com/en/prod/Content/Topics/integrations/getting-started.htm)
  are required.
  High disk throughput is not required), and
- [ERP](https://en.wikipedia.org/wiki/Enterprise_resource_planning)
  (we use two disks:
  a 50 GiB GP2 disk
  for hosting the base operating system
  and a 200 GiB GP2 disk
  for hosting the ERP data).

## Guidelines

- You can access the AWS EBS console
  after [authenticating to AWS](/development/stack/aws#guidelines).
- Any changes to EBS's infrastructure
  must be done
  via [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
- To learn how to test and apply infrastructure
  via [Terraform](/development/stack/terraform),
  visit the [Terraform Guidelines](/development/stack/terraform#guidelines).

[OS]: https://en.wikipedia.org/wiki/Operating_system
[GP2]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.htm
[EBS]: https://aws.amazon.com/ebs/
