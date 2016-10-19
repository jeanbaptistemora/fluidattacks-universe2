
export PROJECT_DIR=$(git rev-parse --show-toplevel)

# Container (docker)
export NET_IP="172.30.216.0/16"
export NET_NAME="fluidasserts"
export SERVICE="alg"
export IP="172.30.216.100"

# Setup (ansible)
export ANSIBLE_HOSTS="$PROJECT_DIR"/provision/hosts
export ANSIBLE_CONFIG="$PROJECT_DIR"/provision/config

# Desahibilitar agentes SSH
export SSH_AUTH_SOCK=0
