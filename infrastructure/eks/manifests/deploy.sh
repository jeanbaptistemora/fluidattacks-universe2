#!/usr/bin/env bash

# Install NGINX Ingress chart to route traffic within the cluster
if ! helm list --tls | grep 'controller'; then
  helm init --client-only
  helm repo update
  helm install stable/nginx-ingress \
    --name controller --namespace serves \
    --set rbac.create=true --tls
fi

# Set TLS certificates in the NGINX server
sed -i 's/$TLS_KEY/'"$FLUID_TLS_KEY"'/;
  s/$FA_TLS_CERT/'"$FLUIDATTACKS_TLS_CERT"'/;
  s/$FLA_TLS_CERT/'"$FLUIDLA_TLS_CERT"'/' \
  eks/manifests/ingress-tls.yaml
kubectl apply -f eks/manifests/ingress-tls.yaml

# Set context to avoid using the --namespace flag in every command
kubectl config set-context $(kubectl config current-context) \
  --namespace serves

# Customize NGINX configuration
kubectl patch cm controller-nginx-ingress-controller \
  --patch "$(cat eks/manifests/nginx-conf.yaml)"

# Provide information to access Gitlab Container Registry and pull images
if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$CI_REGISTRY" --docker-username="$DOCKER_USER" \
    --docker-password="$DOCKER_PASS" --docker-email="$DOCKER_EMAIL"
fi

# Pass variables to Integrates to access Vault
INTEGRATES_VAULT_TOKEN=$(curl --request POST \
  --data '{"role_id":"'"$INTEGRATES_PROD_ROLE_ID"'","secret_id":"'"$INTEGRATES_PROD_SECRET_ID"'"}' \
  "https://$VAULT_S3_BUCKET.com/v1/auth/approle/login" | \
  jq -r '.auth.client_token')
sed -i 's/$VAULT_HOST/'"$(echo -n $VAULT_HOST | base64)"'/;
  s/$INTEGRATES_VAULT_TOKEN/'"$(echo -n $INTEGRATES_VAULT_TOKEN | base64)"'/' \
        eks/manifests/integrates.yaml

# Deploy apps containers
sed -i 's/$DATE/'"$(date)"'/' eks/manifests/*.yaml
kubectl apply -f eks/manifests/alg.yaml
kubectl rollout status deploy/alg -w

kubectl apply -f eks/manifests/exams.yaml
kubectl rollout status deploy/exams -w

kubectl apply -f eks/manifests/integrates.yaml
kubectl rollout status deploy/integrates -w

kubectl apply -f eks/manifests/vpn.yaml
kubectl rollout status deploy/vpn -w

# Wait until the initialization of the Load Balancer is complete
sleep 5
ELB_NAME="$(aws --region us-east-1 elb describe-load-balancers \
  | jq -r '.LoadBalancerDescriptions[].LoadBalancerName')"
ELB_STATUS="$(aws --region us-east-1 elb describe-instance-health \
  --load-balancer-name $ELB_NAME | jq -r '.InstanceStates[].State')"
I=0
while [ "$ELB_STATUS" != "InService" ]; do
  echo 'Waiting for Load Balancer to be ready...'
  sleep 10
  ELB_STATUS="$(aws --region us-east-1 elb describe-instance-health \
  --load-balancer-name $ELB_NAME | jq -r '.InstanceStates[].State')"
  I="$((I+1))"
  if [[ "$I" == 10 ]]; then
    echo "Load Balancer failed the Health Checks and is out of service."
    exit 1
  fi
done
echo 'Load Balancer is ready to receive requests.'
