#! /bin/sh

# Make disk gpt and create partitions
parted /dev/nvme1n1 --script -- mklabel gpt
parted -a optimal /dev/nvme1n1 mkpart primary 0% 65%
parted -a optimal /dev/nvme1n1 mkpart primary 65% 100%

# Wait for partitions to be visible
sleep 1

# Make partitions xfs
mkfs -t xfs /dev/nvme1n1p1
mkfs -t xfs /dev/nvme1n1p2

# Mount partitions
mkdir -p /var/lib/docker
mkdir -p /builds
mount /dev/nvme1n1p1 /var/lib/docker
mount /dev/nvme1n1p2 /builds
