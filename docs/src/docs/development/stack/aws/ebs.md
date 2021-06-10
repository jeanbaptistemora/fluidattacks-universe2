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
    and a throughput of 4000
    [MB/s](https://en.wikipedia.org/wiki/Data-rate_units#Megabyte_per_second)
    to
    [HHDs](https://en.wikipedia.org/wiki/Hard_disk_drive)
    with a size of 16
    [TB](https://en.wikipedia.org/wiki/Byte#Multiple-byte_units)
    and a throughput of 500
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

1. [Gitlab CI](/development/stack/gitlab-ci)
    bastion:
    We use a 16 GB
    [GP2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
    disk,
    as it only needs having basic software installed
    like
    [Gitlab Runner](https://docs.gitlab.com/runner/install/)
    and
    [Docker Machine](https://docs.docker.com/machine/install-machine/).
    High disk throughput is not required.
1. [Gitlab CI workers](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/makes/ci/src/config.toml#L57):
    We use 10 GB
    [GP3](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
    disks just for hosting our workers'
    [Operating system](https://en.wikipedia.org/wiki/Operating_system).
    Aditionally,
    workers come with
    high throughput
    [50 GB internal NVMe disks](https://aws.amazon.com/blogs/aws/ec2-instance-update-c5-instances-with-local-nvme-storage-c5d/),
    which are very useful
    for achieving as-fast-as-possible
    job performence within our [CI](/development/stack/gitlab-ci).
1. [Batch](https://aws.amazon.com/batch/)
    processing
    [workers](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/makes/compute/src/terraform/aws_batch.tf#L112):
    Just like with our
    [CI workers](https://gitlab.com/fluidattacks/product/-/blob/master/makes/applications/makes/ci/src/config.toml#L57),
    we use 8 GB
    [GP2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
    disks just for hosting the
    [Operating system](https://en.wikipedia.org/wiki/Operating_system).
    These workers also come with
    [50 GB internal NVMe disks](https://aws.amazon.com/blogs/aws/ec2-instance-update-c5-instances-with-local-nvme-storage-c5d/).
1. [Kubernetes](/development/stack/kubernetes)
    cluster
    [workers](https://gitlab.com/fluidattacks/product/-/blob/53879d903b3c8c2561d45552cbc53f2350601e38/makes/applications/makes/k8s/src/terraform/cluster.tf#L40):
    We use 50 GB
    [GP2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
    disks for hosting the base
    [Operating system](https://en.wikipedia.org/wiki/Operating_system)
    and stored containers for applications like our
    [ASM](https://fluidattacks.com/categories/asm/).
    High disk thoughput is not required as our
    [ASM](https://fluidattacks.com/categories/asm/)
    does not store any data within local disks.
1. [Okta RADIUS Agent](/development/stack/okta#usage):
    We use a 50 GB
    [GP2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
    disk.
    It is probably oversized as only the base
    [Operating system](https://en.wikipedia.org/wiki/Operating_system)
    and
    [RADIUS agent](https://help.okta.com/en/prod/Content/Topics/integrations/getting-started.htm)
    are required.
    High disk thoughput is not required.
1. [ERP](https://en.wikipedia.org/wiki/Enterprise_resource_planning):
    We use two disks,
    a 50 GB
    [GP2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
    disk for hosting the base
    [Operating system](https://en.wikipedia.org/wiki/Operating_system)
    and a 200 GB
    [GP2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html)
    disk for hosting the
    [ERP](https://en.wikipedia.org/wiki/Enterprise_resource_planning)
    data.

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
