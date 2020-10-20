FROM nixos/nix:2.3

# Base dependencies
RUN apk add --no-cache \
      bash=5.0.0-r0 \
      git=2.22.4-r0

# Timezone
RUN     apk add --no-cache tzdata=2020c-r0 \
    &&  cp /usr/share/zoneinfo/America/Bogota /etc/localtime \
    &&  echo 'America/Bogota' > /etc/timezone \
    &&  apk del tzdata

WORKDIR /product

# Cache integrates dependencies
COPY . .
RUN     nix-shell --run ':' 'build/provisioners/integrates_serve_back_dev.nix' \
    &&  nix-store --optimise
