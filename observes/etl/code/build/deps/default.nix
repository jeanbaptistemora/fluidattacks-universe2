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

  override_1 = python_pkgs:
    python_pkgs
    // {
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      import-linter = import ./import-linter {
        inherit lib python_pkgs;
      };
      pathos = import ./pathos {
        inherit lib python_pkgs;
      };
      redshift-client = nixpkgs.redshift-client."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };

  compose = functions: val: builtins.foldl' (x: f: f x) val functions;
  final_pkgs = compose [override_1] (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
