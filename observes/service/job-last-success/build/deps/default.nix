# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  python_pkgs =
    nixpkgs."${python_version}Packages"
    // {
      types-psycopg2 = import ./psycopg2/stubs.nix lib;
      import-linter = import ./import-linter {
        inherit lib python_pkgs;
      };
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      redshift-client = nixpkgs.redshift-client."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };
in {inherit python_pkgs lib;}
