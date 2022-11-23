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
  pycheck_override = python_pkgs: (import ./pkg_override.nix) (x: (x ? name && x.name == "pytest-check-hook")) python_pkgs.pytestCheckHook;
  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  requests_override = python_pkgs: pkg_override ["requests"] python_pkgs.requests;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;
  overrides = map pkgs_overrides [
    pytz_override
    requests_override
    pycheck_override
  ];

  # layers
  layer_1 = python_pkgs:
    python_pkgs
    // {
      pytz = import ./pytz lib python_pkgs;
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
      requests = import ./requests {inherit lib python_pkgs;};
      types-requests = import ./requests/stubs.nix {inherit lib python_pkgs;};
      legacy-purity = nixpkgs.legacy-purity."${python_version}".pkg;
      legacy-paginator = nixpkgs.legacy-paginator."${python_version}".pkg;
      legacy-singer-io = nixpkgs.legacy-singer-io."${python_version}".pkg;
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
