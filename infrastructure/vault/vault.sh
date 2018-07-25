#!/usr/bin/env bash
set -e

BC='\033[1;34m'
NC='\033[0m'

# Install Vault chart if not present, along the Etcd Chart
# for data storage
if ! helm list --tls | grep 'vault'; then
  helm init --client-only
  helm repo update
  helm install stable/vault-operator --name vault --tls \
    --set etcd-operator.enabled=true \
    --set serviceAccount.name='vault-sa' \
    --set rbac.apiVersion='v1alpha1' 
fi
echo -e "${BC}Vault-Operator successfully installed!${NC}"

# Generate assets for TLS communication with Vault
export KUBE_NS=serves
export SERVER_SECRET=vault-server-tls
export CLIENT_SECRET=vault-client-tls
export SAN_HOSTS="vault.fluidattacks.com"
export SERVER_CERT=server.crt
export SERVER_KEY=server.key
if ! kubectl get secrets | egrep 'vault-(client|server)'; then
  tls-gen.sh
fi
echo -e "${BC}Assets for TLS communication with Vault successfully" \
  "generated!${NC}"

# Download generated CA certificate to the local machine for TLS verification
echo -e "${BC}Obtaining CA certificate...${NC}"
kubectl get secret "$CLIENT_SECRET" -o jsonpath='{.data.*}' | \
  base64 -d > $HOME/vault-ca.crt
export VAULT_CACERT=$HOME/vault-ca.crt

# Deploy Vault instance
echo -e "${BC}Deploying Vault instance...${NC}"
kubectl apply -f vault.yaml
while ! kubectl get pods | egrep --color -o 'vault.*1\/2'; do
  echo -e "${BC}Waiting for pods to be ready...${NC}"
  sleep 5
done
sleep 10
echo -e "${BC}Vault pods are ready!${NC}"

# Deploy secret to allow TLS communication through NGINX controller
# (which uses keyword 'tls' instead of 'server', the later used by Vault)
echo -e "${BC}Provisioning certificates for TLS communication with" \
  "NGINX...${NC}"
kubectl get secret "$SERVER_SECRET" -o jsonpath='{.data.server\.crt}' | \
  xargs -I {} sed -i 's/TLS_CRT/'{}'/' tls.yaml
kubectl get secret "$SERVER_SECRET" -o jsonpath='{.data.server\.key}' | \
  xargs -I {} sed -i 's/TLS_KEY/'{}'/' tls.yaml
kubectl apply -f tls.yaml

# Forward port of Vault pod to initialize and unseal so it can be accessed 
# through the Ingress
echo -e "${BC}Initializing Vault...${NC}"
SEALED=$(kubectl get vault vault -o jsonpath='{.status.vaultStatus.sealed[0]}')
if [ ! -z "$SEALED" ] ; then
  export VAULT_ADDR='https://localhost:8200'
  kubectl get vault vault -o jsonpath='{.status.vaultStatus.sealed[0]}' | \
    xargs -0 -I {} kubectl port-forward {} 8200 &
  sleep 10

  # Initialize and unseal Vault
  vault operator init -key-shares=1 -key-threshold=1 > vault.txt
  export VAULT_KEY=$(cat vault.txt | grep -Po '(?<=Key 1: ).*')
  export VAULT_TOKEN=$(cat vault.txt | grep -Po '(?<=Token: ).*')
  rm vault.txt

  aws --region "us-east-1" secretsmanager list-secrets > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    aws --region "us-east-1" secretsmanager put-secret-value \
      --secret-id "VAULT_KEY" \
      --secret-string "$VAULT_KEY" > /dev/null
    aws --region "us-east-1" secretsmanager put-secret-value \
      --secret-id "VAULT_TOKEN" \
      --secret-string "$VAULT_TOKEN" > /dev/null
    echo -e "${BC}Vault secrets successfully updated!${NC}"
  else
    aws --region "us-east-1" secretsmanager create-secret \
      --name "VAULT_KEY" \
      --description 'Master key to unseal Vault' \
      --secret-string "$VAULT_KEY" > /dev/null
    aws --region "us-east-1" secretsmanager create-secret \
      --name "VAULT_TOKEN" \
      --description 'Vault root token' \
      --secret-string "$VAULT_TOKEN" > /dev/null
    echo -e "${BC}Vault secrets successfully created!${NC}"
  fi
  vault operator unseal "$VAULT_KEY"
  pkill kubectl
fi
echo -e "${BC}Vault unsealed successfully!${NC}"

kubectl apply -f ingress.yaml
