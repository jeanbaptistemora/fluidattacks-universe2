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

  pytz_override = python_pkgs: pkg_override ["pytz"] python_pkgs.pytz;
  purity_override = python_pkgs: pkg_override ["fa_purity"] python_pkgs.fa-purity;
  overrides = map pkgs_overrides [
    pytz_override
    purity_override
  ];

  # layers
  layer_1 = python_pkgs: let
    common_in = {inherit lib python_pkgs;};
  in
    python_pkgs
    // {
      pytz = import ./pytz common_in;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      import-linter = import ./import-linter common_in;
      legacy-paginator = nixpkgs.legacy-paginator."${python_version}".pkg;
      legacy-singer-io = nixpkgs.legacy-singer-io."${python_version}".pkg;
      mypy-boto3-s3 = import ./boto3/s3-stubs.nix common_in;
      types-boto3 = import ./boto3/stubs.nix common_in;
      types-cachetools = import ./cachetools/stubs.nix {inherit lib;};
      types-click = import ./click/stubs.nix {inherit lib;};
      types-python-dateutil = import ./dateutil/stubs.nix {inherit lib;};
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };

  # integrate all
  compose = let
    apply = x: f: f x;
  in
    functions: val: builtins.foldl' apply val functions;
  final_pkgs = compose ([layer_1] ++ overrides) (nixpkgs."${python_version}Packages");
in {
  inherit lib;
  python_pkgs = final_pkgs;
}
