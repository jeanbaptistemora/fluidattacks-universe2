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
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  pycheck_override = python_pkgs: (import ./pkg_override.nix) (x: (x ? name && x.name == "pytest-check-hook")) python_pkgs.pytestCheckHook;
  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  jsonschema_override = python_pkgs: pkg_override ["jsonschema"] python_pkgs.jsonschema;
  overrides = map pkgs_overrides [
    pycheck_override
    pytz_override
    jsonschema_override
  ];

  # layers
  layer_1 = python_pkgs:
    python_pkgs
    // {
      pytz = import ./pytz {inherit lib python_pkgs;};
      jsonschema = import ./jsonschema {inherit lib python_pkgs;};
    };

  layer_2 = python_pkgs:
    python_pkgs
    // {
      pytestCheckHook = python_pkgs.pytestCheckHook.override {
        pytest = pytz_override python_pkgs python_pkgs.pytest;
      };
    };

  layer_3 = python_pkgs:
    python_pkgs
    // {
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      mypy-boto3-s3 = import ./boto3/s3-stubs.nix {inherit lib python_pkgs;};
      types-boto3 = import ./boto3/stubs.nix {inherit lib python_pkgs;};
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };

  # integrate all
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_pkgs = compose ([layer_1 layer_2 layer_3] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
