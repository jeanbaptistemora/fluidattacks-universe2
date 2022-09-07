# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  legacyPkgs,
  lib,
  pythonPkgs,
  pythonVersion,
  system,
}: let
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "2efa874f92fe3ece5d05f3a32a928feb5dee97f6";
    ref = "refs/tags/v1.13.0";
  };
  purity = import purity_src {
    inherit system;
    legacy_pkgs = legacyPkgs;
    src = purity_src;
  };
  returns = import ./returns {
    inherit lib pythonPkgs;
  };
in
  pythonPkgs
  // {
    inherit returns;
    fa-purity = purity."${pythonVersion}".pkg;
  }
