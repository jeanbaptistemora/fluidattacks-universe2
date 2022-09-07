# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  local_pkgs,
  pkgs,
  python_version,
}: let
  python_pkgs = pkgs."${python_version}Packages";
in
  python_pkgs
  // {
    types-click = import ./click/stubs.nix lib;
    types-psycopg2 = import ./psycopg2/stubs.nix lib;
    import-linter = import ./import-linter {
      inherit lib python_pkgs;
    };
    fa-purity = local_pkgs.fa-purity."${python_version}".pkg;
    redshift-client = local_pkgs.redshift-client."${python_version}".pkg;
    utils-logger = local_pkgs.utils-logger."${python_version}".pkg;
  }
