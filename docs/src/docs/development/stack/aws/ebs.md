---
id: ebs
title: Elastic Block Store (EBS)
sidebar_label: EBS
slug: /development/stack/aws/ebs
---

## Rationale

[AWS EBS](https://aws.amazon.com/ebs/)
is the service we use
for [Block-level storage](https://en.wikipedia.org/wiki/Block-level_storage).
It allows us to have
[hard drives](https://en.wikipedia.org/wiki/Device_file#BLOCKDEV)
in the [cloud](https://en.wikipedia.org/wiki/Cloud_computing).

The main reasons why we chose it
over other alternatives are:

1. It seamlessly integrates with
    [AWS EC2](/development/stack/aws/ec2),
    allowing to connect external hard drives
    to instances.
1. It provides a wide range of
    [disk types](https://aws.amazon.com/ebs/features/#Amazon_EBS_volume_types)
    that goes from
    [SSDs](https://en.wikipedia.org/wiki/Solid-state_drive)
    with a size of 64
    [TB](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units)
    and a thoughput of 4000
    [MB/s](https://en.wikipedia.org/wiki/Data-rate_units#Megabyte_per_second)
    to
    [HHDs](https://en.wikipedia.org/wiki/Hard_disk_drive)
    with a size of 16
    [TB](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units)
    and a thoughput of 500
    [MB/s](https://en.wikipedia.org/wiki/Data-rate_units#Megabyte_per_second).
1. Disks are also divided into
    [different specializations](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html).
    There are
    General purpose and Provisioned IOPS
    [SSDs](https://en.wikipedia.org/wiki/Solid-state_drive)
    and
    Throughput Optimized
    and
    Cold
    [HHDs](https://en.wikipedia.org/wiki/Hard_disk_drive).
    By having all these
    different types of disks,
    we can easily select
    which ones to work with
    depending on the nature
    of the problem we are trying to solve.
1. It supports
    [point-in-time snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html)
    designed to backing up all the data
    that exists
    within a disk.
1. Disks can be easily
    [attached](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-attaching-volume.html)
    and
    [detached](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-detaching-volume.html)
    from
    [AWS EC2](/development/stack/aws/ec2) machines,
    allowing to easily change general machine configurations
    without losing any data.
1. Disks can be
    [encrypted](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSEncryption.html)
    using
    [AWS KMS](https://aws.amazon.com/kms/)
    keys, allowing to encrypt
    data moving between the disk and the instance that is using it,
    data at rest inside the volume,
    disk snapshots,
    and all volumes created from those snapshots.
1. It supports
    [data lifecyle policies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/snapshot-lifecycle.html),
    allowing to
    create, retain and delete
    disks based on created policies.
1. It supports
    [monitoring and metrics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using_cloudwatch_ebs.html)
    using
    [AWS CloudWatch](https://aws.amazon.com/cloudwatch/).

## Alternatives

1. [Google Compute Engine](https://cloud.google.com/compute):
    It did not exist at the time we migrated to the cloud.
    [GCP](https://cloud.google.com/gcp)
    does not offer an equivalent to
    [EBS](https://aws.amazon.com/ebs/).
    Instead, their entire
    [disks service](https://cloud.google.com/compute/docs/disks)
    exists within
    [GCE](https://cloud.google.com/compute).
    It does not support disk encryption.
1. [Azure Disk Storage](https://azure.microsoft.com/en-us/services/storage/disks/):
    It did not exist at the time we migrated to the cloud.
    Pending to review.

## Usage

We use [AWS EBS](https://aws.amazon.com/ebs/) for:

1. Managing the base
    [Operating system](https://en.wikipedia.org/wiki/Operating_system)
    of our [Gitlab CI](/development/stack/gitlab-ci)
    bastion and
    [workers](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/makes/ci/src/config.toml#L57).
1. Managing the base
    [Operating system](https://en.wikipedia.org/wiki/Operating_system)
    of our [Batch](https://aws.amazon.com/batch/)
    processing
    [workers](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/makes/compute/src/terraform/aws_batch.tf#L112).
1. Managing the main disk
    of our
    [Kubernetes](/development/stack/kubernetes)
    cluster
    [workers](https://gitlab.com/fluidattacks/product/-/blob/53879d903b3c8c2561d45552cbc53f2350601e38/makes/applications/makes/k8s/src/terraform/cluster.tf#L40).
1. Managing the main disk
    of our
    [Okta RADIUS Agent](/development/stack/okta#usage).
1. Managing the main disk
    of our
    [ERP](https://en.wikipedia.org/wiki/Enterprise_resource_planning).

## Guidelines

1. You can access the
    [AWS EBS](https://aws.amazon.com/ebs/) console
    after [authenticating on AWS](/development/stack/aws#guidelines).
1. Any changes to
    [EBS's](https://aws.amazon.com/ebs/)
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/).
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).
