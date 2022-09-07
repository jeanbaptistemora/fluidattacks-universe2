# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  pkgs,
  inputs,
}: let
  builders.pythonRequirements = import ../../../build/builders/python-requirements pkgs;
  base = [
    pkgs.git
    pkgs.awscli
    pkgs.sops
    pkgs.jq
    pkgs.cacert
  ];
in
  pkgs.stdenv.mkDerivation (
    (import ../../../build/src/basic.nix)
    // (import ../../../build/src/external.nix pkgs)
    // rec {
      name = "builder";

      buildInputs = base ++ inputs;

      pyPkgTestrequirements = builders.pythonRequirements ./tests.lst;
      pyPkgAsserts = import ../.. pkgs;
    }
  )
