FROM nixos/nix:2.3

RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.2-r0

COPY . /code

# Fetch all dependencies to the /nix/store
RUN     nix-shell --run ':' /code/build/shell.nix \
    &&  nix-shell --run 'pushd front && npm install' /code/build/shell.nix \
    &&  nix-shell --run 'pushd mobile && npm install' /code/build/shell.nix \
    &&  nix-store --optimise
