# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  nixpkgs,
  python_version,
}: let
  python_pkgs = nixpkgs."${python_version}Packages";

  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  override_1 = python_pkgs:
    python_pkgs
    // {
      fa-purity = nixpkgs.fa_purity."${python_version}".pkg;
      redshift-client = nixpkgs.redshift_client."${python_version}".pkg;
    };
  # Integrate all
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_nixpkgs = compose [override_1] python_pkgs;
in {
  inherit lib;
  python_pkgs = final_nixpkgs;
}
