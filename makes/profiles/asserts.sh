#! /bin/sh

    nix-env \
      --uninstall asserts \
&&  nix-env \
      --install asserts \
      --file "https://gitlab.com/fluidattacks/product/-/archive/${1:-master}.tar.gz" \
      --option narinfo-cache-negative-ttl 1 \
      --option narinfo-cache-positive-ttl 1 \
      --option restrict-eval false \
      --option sandbox false \
      --option substituters 'https://fluidattacks.cachix.org https://cache.nixos.org' \
      --option trusted-public-keys '
        fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=
        cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY=
      ' \

