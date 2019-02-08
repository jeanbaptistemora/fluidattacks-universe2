FROM registry.gitlab.com/fluidsignal/serves:base

LABEL mantainer="engineering@fluidattacks.com"

WORKDIR /root/

ADD . /root/

ARG VAULT_HOST
ARG VAULT_PORT
ARG VAULT_API_URL
ARG ROLE_ID
ARG SECRET_ID

RUN export VAULT_TOKEN=$(curl \
        --request POST \
        --data '{"role_id":"'"${ROLE_ID}"'","secret_id":"'"${SECRET_ID}"'"}' \
        "${VAULT_API_URL}" | jq -r '.auth.client_token') \
    && vaultenv \
        --host "${VAULT_HOST}" \
        --port "${VAULT_PORT}" \
        --secrets-file ./env.vars \
        ./build.sh \
    && curl \
        --request POST \
        --header "X-Vault-Token: ${VAULT_TOKEN}" \
        "https://${VAULT_HOST}/v1/auth/token/revoke-self"

EXPOSE 443

CMD run
