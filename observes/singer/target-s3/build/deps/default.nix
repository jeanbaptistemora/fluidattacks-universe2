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
  filelock_override = python_pkgs: pkg_override ["filelock"] python_pkgs.filelock;
  overrides = map pkgs_overrides [
    pycheck_override
    pytz_override
    filelock_override
  ];

  # layers
  layer_1 = python_pkgs:
    python_pkgs
    // {
      pytz = import ./pytz {inherit lib python_pkgs;};
      filelock = python_pkgs.filelock.overridePythonAttrs (
        # TODO: only skip tests that relies on env
        _: {doCheck = false;}
      );
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

  # final_pkgs
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_pkgs = compose ([layer_1 layer_2 layer_3] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
