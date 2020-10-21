FROM nixos/nix:2.3

# Base dependencies
RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.4-r0

WORKDIR /product

# Cache integrates dependencies
ARG PROVISIONER
COPY . .
RUN     nix-shell --run ':' "${PROVISIONER}" \
    &&  nix-store --optimise
