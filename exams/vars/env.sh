export SERVICE="exams"

export PROJECT_DIR=$(git rev-parse --show-toplevel)/"$SERVICE"

# Container (docker)
export IP="127.0.0.1"

# Setup (ansible)
export ANSIBLE_HOSTS="$PROJECT_DIR"/provision/hosts
export ANSIBLE_CONFIG="$PROJECT_DIR"/provision/config

# Desahibilitar agentes SSH
export SSH_AUTH_SOCK=0
