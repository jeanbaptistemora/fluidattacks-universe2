# shellcheck disable=SC2148
# Make disk gpt and create partition
yum install -y parted
parted /dev/nvme1n1 --script -- mklabel gpt
parted -a optimal /dev/nvme1n1 mkpart primary 0% 100%

# Wait for partition to be visible
sleep 1

# Make partition xfs
mkfs -t xfs /dev/nvme1n1p1

# Mount partition keeping existing docker files
mv /var/lib/docker /tmp/
mkdir -p /var/lib/docker
mount /dev/nvme1n1p1 /var/lib/docker
mv /tmp/docker/* /var/lib/docker/
