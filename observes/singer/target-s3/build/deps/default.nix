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
  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;

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
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      grimp = import ./grimp {
        inherit lib python_pkgs;
      };
      mypy-boto3-s3 = import ./boto3/s3-stubs.nix lib python_pkgs;
      types-boto3 = import ./boto3/stubs.nix lib python_pkgs;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };
  override_4 = python_pkgs:
    python_pkgs
    // {
      import-linter = import ./import-linter {
        inherit lib python_pkgs;
      };
    };
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [
    pycheck_override
    pytz_override
  ];
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_pkgs = compose ([override_1 override_2 override_3 override_4] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
