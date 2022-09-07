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
  pkg_override = names: (import ./pkg_override.nix) (x: (x ? overridePythonAttrs && builtins.elem x.pname names));
  pycheck_override = python_pkgs: (import ./pkg_override.nix) (x: (x ? name && x.name == "pytest-check-hook")) python_pkgs.pytestCheckHook;

  override_1 = python_pkgs:
    python_pkgs
    // {
      pytz = import ./pytz lib python_pkgs;
    };

  override_2 = python_pkgs:
    python_pkgs
    // {
      pytestCheckHook = python_pkgs.pytestCheckHook.override {
        pytest = pytz_override python_pkgs python_pkgs.pytest;
      };
    };

  override_3 = python_pkgs:
    python_pkgs
    // {
      requests = import ./requests {inherit lib python_pkgs;};
      types-requests = import ./requests/stubs.nix {inherit lib python_pkgs;};
      pytz = import ./pytz lib python_pkgs;
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      mailchimp-transactional = import ./mailchimp-transactional {
        inherit lib python_pkgs;
      };
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };

  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  requests_override = python_pkgs: pkg_override ["requests"] python_pkgs.requests;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [
    pycheck_override
    pytz_override
    requests_override
  ];
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_pkgs = compose ([override_1 override_2 override_3] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
