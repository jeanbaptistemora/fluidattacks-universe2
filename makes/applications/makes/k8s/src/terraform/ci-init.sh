# shellcheck shell=bash
# Make disk gpt and create partition
yum install -y parted
parted /dev/nvme1n1 --script -- mklabel gpt
parted -a optimal /dev/nvme1n1 mkpart primary 0% 65%
parted -a optimal /dev/nvme1n1 mkpart primary 65% 100%

# Wait for partition to be visible
sleep 1

# Make partition xfs
mkfs -t xfs /dev/nvme1n1p1
mkfs -t xfs /dev/nvme1n1p2

# Mount docker partition keeping existing docker files
mv /var/lib/docker /tmp/
mkdir -p /var/lib/docker
mount /dev/nvme1n1p1 /var/lib/docker
mv /tmp/docker/* /var/lib/docker/

# Mount builds partition
mkdir -p /builds
mount /dev/nvme1n1p2 /builds
