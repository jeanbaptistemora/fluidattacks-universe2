#! /usr/bin/env nix-shell
#!   nix-shell -i bash
#!   nix-shell --pure
#!   nix-shell --cores 0
#!   nix-shell --max-jobs auto
#!   nix-shell --attr releaseToPyPi
#!   nix-shell --keep buildFluidassertsRelease
#!   nix-shell --keep TWINE_USERNAME
#!   nix-shell --keep TWINE_PASSWORD
#!   nix-shell ./build-src/main.nix
#  shellcheck shell=bash

source "${genericShellOptions}"

twine check "${buildFluidassertsRelease}/"*
twine upload "${buildFluidassertsRelease}/"*
