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
  # overrides
  pkg_override = names: (import ./pkg_override.nix) (x: (x ? overridePythonAttrs && builtins.elem x.pname names));
  typing_ext_override = python_pkgs: pkg_override ["typing-extensions" "typing_extensions"] python_pkgs.typing-extensions;
  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  jsonschema_override = python_pkgs: pkg_override ["jsonschema"] python_pkgs.jsonschema;
  fa_purity_override = python_pkgs: pkg_override ["fa_purity"] python_pkgs.fa-purity;

  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [
    typing_ext_override
    pytz_override
    jsonschema_override
    fa_purity_override
  ];
  # layers
  layer_1 = python_pkgs:
    python_pkgs
    // {
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      jsonschema = import ./jsonschema {inherit lib python_pkgs;};
      pytz = import ./pytz {inherit lib python_pkgs;};
      snowflake-connector-python = import ./snowflake-connector-python {inherit lib python_pkgs;};
      typing-extensions = import ./typing-extensions {inherit lib python_pkgs;};
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };
  # integrate all
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_nixpkgs = compose ([layer_1] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_nixpkgs;
}
