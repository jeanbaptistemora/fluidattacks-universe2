FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.2-r0

COPY ./build/include                 /build/include
COPY ./build/modules                 /build/modules
COPY ./build/pkgs                    /build/pkgs
COPY ./build/shell.nix               /build/shell.nix

# Fetch all dependencies to the /nix/store
RUN nix-shell --run ':' /build/shell.nix
