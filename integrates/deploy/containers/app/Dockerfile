# Inherit from base
ARG BASE
FROM ${BASE}

# Rebuild integrates dependencies
ARG PROVISIONER
WORKDIR /product
COPY . .
RUN     nix-shell --run ':' "${PROVISIONER}" \
    &&  nix-store --optimise
