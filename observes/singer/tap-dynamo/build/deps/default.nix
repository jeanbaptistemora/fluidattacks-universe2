{
  nixpkgs,
  python_version,
}: let
  python_pkgs = nixpkgs."${python_version}Packages";
  pkg_override = names: (import ./pkg_override.nix) (x: (x ? overridePythonAttrs && builtins.elem x.pname names));

  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  # Layer 1
  override_1 = python_pkgs:
    python_pkgs
    // {
      mypy-boto3-dynamodb = import ./boto3/dynamodb-stubs.nix {inherit lib python_pkgs;};
      pytz = import ./pytz {
        inherit lib python_pkgs;
      };
      types-boto3 = import ./boto3/stubs.nix {inherit lib python_pkgs;};
      types-click = import ./click/stubs.nix {inherit lib;};
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };
  # Layer 2
  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  pycheck_override = python_pkgs: (import ./pkg_override.nix) (x: (x ? name && x.name == "pytest-check-hook")) python_pkgs.pytestCheckHook;
  override_2 = let
    _fa_purity = import ./fa-purity {
      inherit nixpkgs;
    };
    _fa_singer_io = import ./fa-singer-io {
      nixpkgs =
        nixpkgs
        // {
          purity = _fa_purity;
        };
    };
  in
    python_pkgs:
      python_pkgs
      // {
        arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
        fa-purity = _fa_purity."${python_version}".pkg;
        fa-singer-io = _fa_singer_io."${python_version}".pkg;
        pytestCheckHook = python_pkgs.pytestCheckHook.override {
          pytest = pytz_override python_pkgs python_pkgs.pytest;
        };
      };
  # Integrate all
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [
    pytz_override
    pycheck_override
  ];
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_nixpkgs = compose ([override_1 override_2] ++ overrides) python_pkgs;
in {
  inherit lib;
  python_pkgs = final_nixpkgs;
}
